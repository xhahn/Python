import os
import pandas as pd
import scipy as sp
import random

NUM = 1000


# 均方误差根
def rmse(y_test, y):
    return sp.sqrt(sp.mean((y_test - y) ** 2))


def getData(sourcePath, dataPath):
    output = open(dataPath, "w")
    output.write("id,ip,date,method,url,protocol,statue,data\n")
    with open(sourcePath) as file:
        count = 0
        while count != NUM:
            line = file.readline()
            if line[-3:-1] == "-1":
                continue
            line = line.replace("<=>", ",")
            output.write(str(count) + ",")
            output.write(line)
            count += 1
    output.close()


def makeMiss(data):
    y = []
    for x in range(NUM // 5):
        y.append(data.iloc[x, -1])
        data.iloc[x, -1] = -1

    return data, y


def hotdeck(dataWithMissing, dataNoMissing):
    dic = {}
    mi = []

    data_mean = 1.0 * dataNoMissing['data'].sum() / len(dataNoMissing)
    for x in range(NUM // 5 * 4):
        dic[dataNoMissing.iloc[x]['url']] = dataNoMissing.iloc[x]['data']

    for x in range(NUM // 5):
        mi.append(dic.get(dataWithMissing.iloc[x]['url'], data_mean))

    return mi


def getVocabSet(line):
    vocabSet = set([])
    vocabSet.add(line[0])
    vocabSet |= set(line[1].split(' '))
    vocabSet.add(line[2])
    vocabSet |= set(line[3].split('/'))
    vocabSet |= set(line[4].split('/'))
    vocabSet.add(line[5])
    vocabSet.add(line[6])
    return vocabSet


def getDistance(vec1, vec2):
    distance = 0
    for x in range(len(vec1)):
        distance += abs(vec1[x] - vec2[x])

    return distance


def getVec(inputSet, vocabList):
    vec = [0] * len(vocabList)

    for word in inputSet:
        if word in vocabList:
            vec[vocabList.index(word)] = 1

    return vec


def knn(dataWithMissing, dataNoMissing):
    mi = []
    vocabSet = set([])
    dataNoMissingVec = list()

    dataWithMissing.dropna(axis=0, how='all')
    dataNoMissing.dropna(axis=0, how='all')
    for line in dataNoMissing.values:
        vocabSet |= getVocabSet(line)

    vocabList = list(vocabSet)

    for line in dataNoMissing.values:
        inputSet = getVocabSet(line)
        vec = getVec(inputSet, vocabList)
        dataNoMissingVec.append(vec)

    for line in dataWithMissing.values:
        inputSet = getVocabSet(line)
        vec = getVec(inputSet, vocabList)

        maxDistance = 0
        index = 0
        liker = 0
        for otherVec in dataNoMissingVec:
            currDistance = getDistance(vec, otherVec)
            if maxDistance < currDistance:
                maxDistance = currDistance
                liker = index
            index += 1
        mi.append(dataNoMissing.iloc[liker]['data'])

    return mi


def rmse(mi, truth):

    for x in range(len(mi)):
        mi[x] = (mi[x]-truth[x]) ** 2
    return sp.sqrt(sp.mean(mi))


if __name__ == '__main__':
    dataPath = "apacheData.csv"
    sourcePath = "apache.txt"
    if not os.path.exists(dataPath):
        getData(sourcePath, dataPath)

    raw_data = pd.read_csv(dataPath)
    target = ['id', 'data']
    predictors = [x for x in raw_data.columns if x not in target]

    data, truth = makeMiss(raw_data)
    dataWithMissing = data.iloc[0:NUM // 5]
    dataNoMissing = data.iloc[NUM / 5:NUM]

    mi_hotdeck = hotdeck(dataWithMissing, dataNoMissing)
    mi_knn = knn(dataWithMissing, dataNoMissing)

    print("hotdeck:")
    print(rmse(mi_hotdeck, truth))
    print("knn:")
    print(rmse(mi_knn, truth))
