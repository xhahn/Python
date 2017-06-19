#Import libraries:
import numpy as np
import sys
import operator
import pandas as pd
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from sklearn import cross_validation, metrics #Additional scklearn funcitons
from sklearn.grid_search import GridSearchCV #Perforing grid search


def modelfit(alg, dtrain, predictors, useTrainCV=True, cv_folds=5, early_stopping_rounds=50):
    if useTrainCV:
        xgb_param = alg.get_xgb_params()
        xgtrain = xgb.DMatrix(dtrain[predictors].values, label=dtrain['target'].values)
        cvresult = xgb.cv(xgb_param, xgtrain, num_boost_round=alg.get_params()['n_estimators'], nfold=cv_folds, metrics='auc', early_stopping_rounds=early_stopping_rounds)
        alg.set_params(n_estimators=cvresult.shape[0])
                         
        #Fit the algorithm on the DataFrame
        alg.fit(dtrain[predictors], dtrain['target'],eval_metric='auc')
                          
        #Predict training set:
        dtrain_predictions = alg.predict(dtrain[predictors])
        dtrain_predprob = alg.predict_proba(dtrain[predictors])[:,1]
                          
        #Print model report:
        print "\nModel Report"
        print "Accuracy : %.4g" % metrics.accuracy_score(dtrain['target'].values, dtrain_predictions)
        print "AUC Score (Train): %f" % metrics.roc_auc_score(dtrain['target'], dtrain_predprob)

        importances = alg.booster().get_fscore()
        importances = sorted(importances.items(), key=operator.itemgetter(1), reverse=True)
        df = pd.DataFrame(importances, columns=['feature', 'fscore'])
        df['fscore'] = df['fscore'] / df['fscore'].sum()

        df.to_csv("ips.csv", index=False)

        feat_imp = pd.Series(alg.booster().get_fscore()).sort_values(ascending=False)
        print feat_imp

def modelGridSearch(train, predictors, target):
    param_test1 = {
        'max_depth':range(3,10,2),
        'min_child_weight':range(1,6,2)
    }

    param_test2 = {
         'gamma':[i/10.0 for i in range(0.5)]
    }

    param_test3 = {
        'subsample':[i/10.0 for i in range(6,10)],
        'colsample_bytree':[i/10.0 for i in range(6,10)],
    }
    gsearch1 = GridSearchCV(estimator = XGBClassifier(learning_rate =0.1, n_estimators=140, max_depth=7, min_child_weight=3, gamma=0, subsample=0.8, colsample_bytree=0.8, objective= 'binary:logistic', scale_pos_weight=1, seed=12), param_grid = param_test1, scoring='roc_auc', n_jobs=4, iid=False, cv=5)
    gsearch1.fit(train[predictors],train[target])
    print gsearch1.grid_scores_, gsearch1.best_params_, gsearch1.best_score_

if __name__ == '__main__':
    train = pd.read_csv(sys.argv[1])
    target = 'target'
    predictors = [x for x in train.columns if x not in [target]]

    xgb1 = XGBClassifier(
        learning_rate = 0.1,
        min_child_weight = 3,
        n_estimators= 100,
        colsample_bytree = 0.8,
        max_depth =  7,
        subsample = 0.8,
        gamma = 0,
        silent = 1,
        seed = 12,
        objective = 'binary:logistic',
    )
    
    modelfit(xgb1, train, predictors)
   # modelGridSearch(train, predictors, target)



