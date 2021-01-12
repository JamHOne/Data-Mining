# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 20:33:03 2021

@author: Altria
"""

import csv
import random 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

flag =False
x=[]
y=[]
filepath ="test.txt"
f =open (filepath,'r')
d=csv.reader(f)
# print (d)
for i,line in enumerate(d):
    
     for n in line:
         if not n :
             flag =True
             break
     if flag == True:
         flag =False
         continue
     
     #line =','.join(str(n) for n in line)
     x.append(line[:])
     y.append(line[-1])
     
     
def get_a_b(x):
    add_x =0
    add_y = 0
    up = 0
    down = 0
    for i in range(len(x)):
        add_x+=float(x[i][0])
        
        add_y+=float(x[i][1])
    mean_x = add_x/len(x)
    mean_y = add_y/len(x)
    for i in range(len(x)):
        mean_x1 = float(x[i][0]) - mean_x
        mean_y1 = float(x[i][1]) - mean_y
        
        up +=mean_x1*mean_y1
        
        down += mean_x1**2
    a = up/down
    b = mean_y - a*mean_x
    return a,b
    
    
a,b = get_a_b(x)  
def get_linear(a,b,x):
    x1=[]
    y1=[]
    for i in range(len(x)):
        x1.append(float(x[i][0]))
        y1.append(float(x[i][1]))
    x1 = np.array(x1)
    y1 = np.array(y1)    
        
    #plt.scatter(x1, y1, c='blue',alpha = 0.2)  #alpha:透明度) c:颜色
    y2 = a*x1+b
    #plt.plot(x1, y2, linewidth=1)  #线宽linewidth=1
    plt.show()
    return y2
y2 = get_linear(a, b, x)    
def get_sigmoid(y2):
   y3 = 1.0 /(1.0 + np.exp(-y2))    
   #plt.plot(y2, y3, linewidth=1)  #线宽linewidth=1
   plt.show() 
get_sigmoid(y2)
y5=[]
x5=[[]for i in range(len(x))]
x_0, x_1, y_0, y_1 = [], [], [], []
for i in range(len(y)):
    if y[i]=='1':
        y5.append(0)
        x_0.append(float(x[i][0]))
        y_0.append(float(x[i][1]))
    else: y5.append(1)  
    x5[i].append(float(x[i][0]))
    x5[i].append(float(x[i][1]))
    x_1.append(float(x[i][0]))
    y_1.append(float(x[i][1]))
    
y5 = np.array(y5)
x5 = np.array(x5)    
dataMat = np.insert(x5, 0, 1, axis=1)
def get_sigmoid1(y2):
    y3 = 1.0 /(1.0 + np.exp(-y2))    
    return y3


def loss_funtion(dataMat, classLabels, weights):
    m, n = np.shape(dataMat)
    loss = 0.0
    for i in range(m):
        sum_theta_x = 0.0
        for j in range(n):
            sum_theta_x += dataMat[i, j] * weights.T[0, j]
        propability = get_sigmoid1(sum_theta_x)
        loss += -classLabels[i, 0] * np.log(propability) - (1 - classLabels[i, 0]) * np.log(1 - propability)
    return loss

def grad_descent(dataMatIn, classLabels):
    dataMatrix = np.mat(dataMatIn)  #(m,n)
    labelMat = np.mat(classLabels).T
    m, n = np.shape(dataMatrix)
    weights = np.ones((n, 1))
    alpha = 0.01
    maxstep = 10000
    eps = 0.0001
    count = 0
    loss_array = []

    for i in range(maxstep):
        loss = loss_funtion(dataMatrix, labelMat, weights)

        h_theta_x = get_sigmoid1(dataMatrix * weights)
        e = h_theta_x - labelMat
        new_weights = weights - alpha * dataMatrix.T * e
        new_loss = loss_funtion(dataMatrix, labelMat, new_weights)
        loss_array.append(new_loss)
        if abs(new_loss - loss) < eps:
            break
        else:
            weights = new_weights
            count += 1

    print ("count is: ", count)
    print ("loss is: ", loss)
    print ("weights is: ", weights)

    return weights, loss_array
weights, loss_array = grad_descent(dataMat, y5)
def paint_1(x_0,x_1,y_0,y_1,weights):
    fig = plt.figure(figsize=(7,6))
    ax = fig.add_subplot(111)#1行1列 
    ax.scatter(x_0,y_0,c='red')
    ax.scatter(x_1,y_1,c='blue')
    x_new = np.arange(1.0,7.0,0.1)
    y_new = (-weights[0]-weights[1]*x_new)/(weights[2])
    y_new =np.mat(y_new).T
    ax.plot(x_new, y_new, 'k--',color = 'black', linewidth=2)
    plt.show()

paint_1(x_0,x_1,y_0,y_1,weights)
