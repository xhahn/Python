import math
import random
import numpy as np

def sigmoid(inX):
    return 1.0/(1+math.exp(-inX))

def stocGradAscent(dataMatrix, classLabels, numIter=500):
    m, n = np.shape(dataMatrix)
    weights = np.ones(n)
    for j in range(numIter):
        dataIndex = list(range(m))
        for i in range(m):
            alpha =4/(1.0+i+j)+0.01
            randIndex = int(random.uniform(0,len(dataIndex)))
            h = sigmoid(sum(dataMatrix[randIndex]*weights))
            error = classLabels[randIndex] - h
            weights = weights + alpha * error * dataMatrix[randIndex]
            del(dataIndex[randIndex])
    return weights

def classifyVector(inX, weights):
    prob = sigmoid(sum(inX*weights))
    if prob > 0.5:
        return 1.0
    return 0.0

def colicTest():
    frTrain = open('horseTrain.txt')
    frTest = open('horseTest.txt')
    trainingSet = []
    trainingLabels = []
    for line in frTrain.readlines():
        currLine = line.strip().split(' ')
        lineArr = []
        for i in range(3):
            if currLine[i]=='?':c='0'
            else:c=currLine[i]
            lineArr.append(float(c))
        for i in range(4,24):
            if currLine[i]=='?':c='0'
            else:c=currLine[i]
            lineArr.append(float(c))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[-1]))
    trainWeights = stocGradAscent(np.array(trainingSet), trainingLabels, 500)
    errorCount = 0
    numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1
        currLine = line.strip().split(' ')
        lineArr = []
        for i in range(3):
            if currLine[i]=='?':c='0'
            else:c=currLine[i]
            lineArr.append(float(c))
        for i in range(4,24):
            if currLine[i]=='?':c='0'
            else:c=currLine[i]
            lineArr.append(float(c))
        if int(classifyVector(np.array(lineArr), trainWeights)) != int(currLine[-1]):
            errorCount += 1
    errorRate = float(errorCount)/numTestVec
    print("the error rate of this test is : %f" % errorRate)
    return errorRate

def multiTest():
    numTest = 10
    errorSum = 0.0
    for k in range(numTest):
        errorSum += colicTest()
    print("after %d iterations the average error rate is : %f" % (numTest, errorSum/float(numTest)))


