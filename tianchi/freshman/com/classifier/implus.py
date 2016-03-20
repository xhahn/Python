import numpy as np

trainData = []
offline_candidate_data = []

for line in open("F:\\acm\\pycharm\\project\\tianchi\\freshman\\source\\trainData.csv"):
    line = line.replace('\n', '')
    array = line.split(',')
    if array[0] == 'user_id':
        continue
    uid = (array[0], array[1], int(array[-1].strip().split(' ')[0].split('-')[2])+1)
    trainData.append(uid)

for line in open("F:\\acm\\pycharm\\project\\tianchi\\freshman\\source\\18.csv"):
    line = line.replace('\n', '')
    array = line.split(',')
    if array[0] == 'user_id':
        continue
    uid = (array[0], array[1], int(array[-1].strip().split(' ')[0].split('-')[2])+1)
    offline_candidate_data.append(uid)

trainData = list(set(trainData))
offline_candidate_data = list(set(offline_candidate_data))

print('training item number:\t%d\n' % len(trainData))
print('offline candidate item number:\t%d\n' % len(offline_candidate_data))

######################################################################################################
import math
ui_dict = [{} for i in range(4)]
ui_buy = {}
# for feature, for this demo, sum of 4 operation
# for label
for line in open("F:\\acm\\pycharm\\project\\tianchi\\freshman\\source\\trainData_dic.csv"):
    line = line.replace('\n', '')
    array = line.split(',')
    if array[0] == 'user_id':
        continue
    day = int(array[-1].split(' ')[0].split('-')[2])
    uid = (array[0], array[1], day)
    type = int(array[2]) - 1
    if uid in ui_dict[type]:
        ui_dict[type][uid] += 1
    else:
        ui_dict[type][uid] = 1
    if type == 3:
        ui_buy[uid] = 1

#get train X, y
X = np.zeros((len(trainData), 4))
y = np.zeros((len(trainData), ))
id =0
for uid in trainData:
    last_uid = (uid[0], uid[1], uid[2] - 1)
    for i in range(4):
        X[id][i] = math.log1p(ui_dict[i][last_uid] if last_uid in ui_dict[i] else 0)
    y[id] = 1 if uid in ui_buy else 0
    id += 1

print("X = ", X, '\n\n', 'y = ', y, '\n\n')
print("train number = %d, positive number = %d"%(len(y), sum(y)))

#get predict pX for offline_candidate_data
pX = np.zeros((len(offline_candidate_data), 4))
id = 0
for uid in offline_candidate_data:
    last_uid = (uid[0], uid[1], uid[2] - 1)
    for i in range(4):
        pX[id][i] = math.log1p(ui_dict[i][last_uid] if last_uid in ui_dict[i] else 0)
    id += 1

### train ##########################
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X, y)

### evaluate ###############################
py = model.predict_proba(pX)
npy = []
for a in py:
    npy.append(a[1])
py = npy

print("px =", pX)

### combine
lx = zip(offline_candidate_data, py)
lx = sorted(lx, key=lambda x:x[1], reverse=True)
print(lx[0])
print(lx[1])
print(lx[2])

wf = open("F:\\acm\\pycharm\\project\\tianchi\\freshman\\source\\tianchi_mobile_recommendation_predict.csv", 'w')
wf.write('user_id,item_id\n')
for i in range(500):
    item = lx[i]
    wf.write('%s,%s\n'%(item[0][0], item[0][1]))
wf.close()
