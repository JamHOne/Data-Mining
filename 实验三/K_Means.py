import pandas as pd
import numpy as np
import random as rd
from collections import Counter
from matplotlib.patches import Circle
import math
import matplotlib.pyplot as plt


# 初始化最开始的聚类点
def random_initialize(dataset,k):
    centroids = np.zeros((k,dataset.shape[1]))
    for i in range(k):
        index = int(rd.uniform(0,dataset.shape[0]))
        centroids[i,:] = dataset[index,:]
    return centroids

# 计算点到聚类点的距离
def CalDistance(dataset,centroids):
    distance = 0
    for i in range(len(dataset)):
        distance+=(dataset[i]-centroids[i])**2
    distance = math.sqrt(distance)
    return distance

def K_Means(dataset,k):
    centroids = random_initialize(dataset,k)
    clusterAssment = np.zeros((dataset.shape[0],1))
    r = {}
    # 迭代标记
    Isbool = True
    while Isbool:
        Isbool = False
        for i in range(dataset.shape[0]):
            minDist = 10000
            minIndex = 0
            for j in range(k):
                distance = CalDistance(dataset[i],centroids[j])
                if distance<minDist:
                    minDist = distance
                    minIndex = j
            #   如果存在还没有优化到最佳的节点，则继续迭代
            if clusterAssment[i] != minIndex:
                Isbool = True
            clusterAssment[i] = minIndex
        for j in range(k):
            new = []
            for x in range(dataset.shape[0]):
                if clusterAssment[x]==j:
                    new.append(dataset[x])
            new = np.array(new)
            # 重新定义聚类点，取聚类后的结果的均值作为新的聚类点
            centroids[j,:] = np.mean(new,axis=0)
    clusterAssment = clusterAssment.astype(int)
    # 计算聚类半径
    for i in range(len(clusterAssment)):
        if clusterAssment[i][0] not in r:
            r[clusterAssment[i][0]] = CalDistance(dataset[i],centroids[clusterAssment[i][0]])
            continue
        if r[clusterAssment[i][0]]<CalDistance(dataset[i],centroids[clusterAssment[i][0]]):
            r[clusterAssment[i][0]] = CalDistance(dataset[i],centroids[clusterAssment[i][0]])
    return centroids,clusterAssment,r

def showCluster(dataSet, k, centroids, clusterAssment,minDist):
    numSamples, dim = dataSet.shape
    if dim != 2:
        print("Sorry! I can not draw because the dimension of your data is not 2!")
        return 1

    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    if k > len(mark):
        print
        "Sorry! Your k is too large! please contact Zouxy"
        return 1

        # draw all samples
    for i in range(numSamples):
        markIndex = int(clusterAssment[i])
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])

    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
    # draw the centroids
    for i in range(k):
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize=12)
    theta = np.arange(0, 2 * np.pi, 0.01)
    for i in range(len(minDist)):
        plt.plot(centroids[i][0] + minDist[i] * np.cos(theta), centroids[i][1] + minDist[i] * np.sin(theta))
    plt.show()

plt.scatter
if __name__=='__main__':
    train = pd.read_csv('test.txt')
    train[train == '_'] = np.nan
    train = train.dropna(axis=0,how='any')
    train = np.array(train)
    train = train.astype(float)

    centroids,clusterAssment,minDist = K_Means(train,2)
    showCluster(train,2,centroids=centroids,clusterAssment=clusterAssment,minDist=minDist)

    with open('result.txt','w') as f:
        for i in range(len(train)):
            result = str(train[i][0])+","+str(train[i][1])+','+str(clusterAssment[i][0])
            f.writelines(result)
            f.write('\n')