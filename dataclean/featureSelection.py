import pandas as pd
import numpy as np
import scipy as sp
from scipy.stats import norm
from sklearn.linear_model import LogisticRegression

NUM = 10000
feature_all = ['date', 'time', 'logid', 'type', 'subtype', 'level', 'vd', 'srcip', 'srcport', 'dstip', 'dstport', 'sessionid', 'proto']
feature_xgboost = ['target', 'dstport', 'dstip', 'srcip', 'srcport', 'vd', 'logid', 'sessionid', 'level', 'proto', 'time']


def getData(dataPath):
    df = pd.read_csv(dataPath)
    return df.iloc[:NUM]

def getPrecision(y_predict, y_test):
    total_num = len(y_predict)
    same_num = 0

    for x in range(total_num):
        if y_predict[x] == y_test[x]:
            same_num += 1
    return same_num/total_num

def lr(train, test):
    y_train = train['target'].values
    y_test = test['target'].values
    x_train = train.dropna(axis=0, how='all').values
    x_test = test.dropna(axis=0, how='all').values


    classifier = LogisticRegression()
    classifier.fit(x_train, y_train)

    y_predict = classifier.predict(x_test)

    p = getPrecision(y_predict, y_test)

    return p

def getXGBoostData(data, num):
    data = data[feature_xgboost[:num]]
    train = data.iloc[:int(NUM*0.7)]
    test = data.iloc[:int(NUM*0.3)]
    return train, test

def fs_xgboost(data):
    print("xgboost:")
    for x in range(2, 10, 2):
        train_xgboost, test_xgboost = getXGBoostData(data, x+1)
        p_xgboost = lr(train_xgboost, test_xgboost)
        print(p_xgboost)

def getSFSData(data, feature):
    data = data[feature]
    train = data.iloc[:int(NUM*0.7)]
    test = data.iloc[:int(NUM*0.3)]
    return train, test

def fs_sfs(data):
    print("sfs:")
    max = 8
    feature = ['target']

    for i in range(max):
        max_p = -1
        curr_feature = ''
        for j in range(len(feature_all)):
            feature.append(feature_all[j])
            train_sfs, test_sfs = getSFSData(data, feature)
            p = lr(train_sfs, test_sfs)
            if p > max_p:
                curr_feature = feature_all[j]
                max_p = p
            feature.remove(feature_all[j])
        feature.append(curr_feature)
        feature_all.remove(curr_feature)
        if i % 2 == 1:
            print(max_p)


if __name__ == '__main__':

    dataPath = 'ips.csv'
    data = getData(dataPath)

    fs_xgboost(data)
    fs_sfs(data)






