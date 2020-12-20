import cx_Oracle
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns

'''
    连接数据库，账号名为cc，密码为Ccpassowrd，使用本地IP进行连接
    数据库名为TESTDATA，从中取出所有数据
'''
db_conn = cx_Oracle.connect("cc","oracle","localhost/orcl")
db_cur = db_conn.cursor()
result = db_cur.execute("select * from TESTDATA")

'''
    使用panda方法读取txt文件，默认分隔符为','，并将其转换为numpy数组
'''
txtData_set = pd.read_csv('data.txt',sep=',')
txtData = np.array(txtData_set)

# 获取列名
title = [i[0] for i in db_cur.description]
result = []

dataLabel = {}

# 数据单位一致
for i in range(0,txtData.shape[1]):
    for j in range(0,txtData.shape[0]):
        if i == title.index('HEIGHT'):
            txtData[j][i] = txtData[j][i]*100
        if i == title.index('ID'):
            txtData[j][i] = txtData[j][i]%1000
        if i == title.index('GENDER'):
            if txtData[j][i] == 'male':
                txtData[j][i] = 'boy'
            if txtData[j][i] == 'female':
                txtData[j][i] = 'girl'

txtData_row = txtData.shape[0]

i = 0

# 数据冗余处理
while(i<txtData_row):
    if txtData[i][title.index('ID')] not in dataLabel:
        dataLabel[txtData[i][title.index('ID')]] = 0
    dataLabel[txtData[i][title.index('ID')]]+=1
    if dataLabel[txtData[i][title.index('ID')]]>1:
        print("出现数据冗余,行数为%d"%(i))
        txtData = np.delete(txtData,i,0)
        i-=1
    txtData_row = txtData.shape[0]
    i+=1

i:int = 0
txtData_row = txtData.shape[0]

# 数据缺失处理
while(i<txtData_row):
    num = i+1
    if num != txtData[i][title.index('ID')]:
        # print(num)
        arr = db_cur.execute('select * from TESTDATA where ID = %s and rownum<2'%num)
        testData = []
        for re in arr:
            re = list(re)
            testData.append(re)
        testData = np.array(testData)
        testData = testData.flatten()
        if testData.shape == ():
            # txtData = np.append(txtData,testData, axis=2)
            txtData = np.row_stack((txtData,testData))
    txtData_row = txtData.shape[0]
    i+=1

txtData[txtData[:,1].argsort()]

i = 0

dataLabel = {}

while(i<txtData_row):
    if txtData[i][title.index('ID')] not in dataLabel:
        dataLabel[txtData[i][title.index('ID')]] = 0
    dataLabel[txtData[i][title.index('ID')]]+=1
    if dataLabel[txtData[i][title.index('ID')]]>1:
        txtData = np.delete(txtData,i,0)
        i-=1
    txtData_row = txtData.shape[0]
    i+=1

txtData = txtData[txtData[:,0].argsort()]

test = []

# 使用字典记录不同体测数值对应的成绩
dic = {'bad':50,'general':65,'good':80,'excellent':90}

for i in range(txtData.shape[0]):
    for j in range(txtData.shape[1]):
        if pd.isna(txtData[i][j]) or txtData[i][j] == None:
            id = txtData[i][title.index('ID')]
            res = db_cur.execute("select %s from TESTDATA where ID = %s"%(title[j],id))
            for re in res:
                re = list(re)
                if re!=None:
                    txtData[i][j] = re[0]


np.savetxt('result.txt',txtData,fmt='%s')

Beijing_avgGrade = {}

# 计算均值
def CalMean(txtData,a,b):
    Study_Avg = []
    countNan = 0
    for i in range(a, b + 1):
        a = 0
        for j in range(txtData.shape[0]):
            if np.isnan(txtData[j][i]):
                countNan += 1
                continue
            a += txtData[j][i]
        a = a / (txtData.shape[0] - countNan)
        Study_Avg.append(a)
    return Study_Avg

# 计算方差
def CalStd(txtData,a,b,mean):
    countNan = 0
    Study_std = []
    for i in range(a, b + 1):
        grade = 0
        for j in range(txtData.shape[0]):
            if np.isnan(txtData[j][i]):
                countNan += 1
                continue
            grade += (txtData[j][i] - mean[i - 5]) ** 2 / (txtData.shape[0] - 1 - countNan)
        Study_std.append(grade)
    return Study_std

# 计算相关系数
def CalZ(txtData, a, b, StudyMean, StudyStd, SportMean, SportStd):
    correletion = []
    z_score = 0
    for i in range(a, b + 1):
        for j in range(txtData.shape[0]):
            if np.isnan(txtData[j][i]):
                z = (txtData[j - 1][i] - StudyMean[i - 5]) / math.sqrt(StudyStd[i - 5]) * (dic[txtData[j][-1]] - SportMean) / SportStd
                continue
            if txtData[j][-1] not in dic:
                continue
            z = (txtData[j][i] - StudyMean[i - 5]) / math.sqrt(StudyStd[i - 5]) * (dic[txtData[j][-1]] - SportMean) / SportStd
        z_score += z
        correletion.append(z_score)
    return correletion

def Caculate(txtData,ProgramNum):
    if ProgramNum==1:
        for i in range(txtData.shape[0]):
            sum = 0
            if txtData[i][title.index('CITY')]:
                for j in range(title.index('C1'),title.index('C9')+1):
                    if j==5 or j==6 or j==7 or j==8 or j==9 or j==10:
                        sum += txtData[i][j]*10
                        break
                    sum+=txtData[i][j]
            avg = sum/10
            Beijing_avgGrade[txtData[i][title.index('NAME')]] = avg
        return Beijing_avgGrade
    if ProgramNum==2:
        counter = 0
        for i in range(txtData.shape[0]):
            if txtData[i][title.index('CITY')]=='Guangzhou' and txtData[i][title.index('C1')]>=80 and txtData[i][title.index('C9')]>=6 and txtData[i][title.index('GENDER')]=='boy':
                counter+=1
        return counter
    if ProgramNum==3:
        GuangzhouList = []
        ShanghaiList = []
        GuangzhouSum = 0
        ShanghaiSum = 0
        for i in range(txtData.shape[0]):
            if txtData[i][title.index('CITY')]=='Guangzhou':
                GuangzhouList.append(txtData[i][title.index('CONSTITUTION')])
            elif(txtData[i][title.index('CITY')])=='Shanghai':
                ShanghaiList.append(txtData[i][title.index('CONSTITUTION')])
        for item in GuangzhouList:
            if item=='bad':
                GuangzhouSum+=50
            elif(item=='general'):
                GuangzhouSum+=65
            elif(item=='good'):
                GuangzhouSum+=80
            elif(item=='excellent'):
                GuangzhouSum+=90
        for item in ShanghaiList:
            if item == 'bad':
                ShanghaiSum += 50
            elif (item == 'general'):
                ShanghaiSum += 65
            elif (item == 'good'):
                ShanghaiSum += 80
            elif (item == 'excellent'):
                ShanghaiSum += 90
        Avg = {'Guangzhou':GuangzhouSum/len(GuangzhouList),'Shanghai':ShanghaiSum/len(ShanghaiList)}
        Avg = sorted(Avg.items(),reverse=False)
        return Avg[0][0]


    if ProgramNum==4:
        z = 0
        countNan = 0
        Sport_Avg = 0
        Study_std = []
        Sport_std = 0
        z_score = 0
        correletion = []

        Study_Avg = CalMean(txtData,title.index('C1'),title.index('C9'))

        for i in range(txtData.shape[0]):
            if txtData[i][title.index('CONSTITUTION')]=='bad':
                Sport_Avg+=50
            elif txtData[i][title.index('CONSTITUTION')]=='general':
                Sport_Avg+=65
            elif txtData[i][title.index('CONSTITUTION')]=='good':
                Sport_Avg+=80
            elif txtData[i][title.index('CONSTITUTION')]=='excellent':
                Sport_Avg+=90

        Sport_Avg = Sport_Avg/txtData.shape[0]

        Study_std = CalStd(txtData,title.index('C1'),title.index('C9'),Study_Avg)
        for i in range(txtData.shape[0]):
            if txtData[i][title.index('CONSTITUTION')] == 'bad':
                Sport_std+=(50-Sport_Avg)**2/txtData.shape[0]
            elif txtData[i][title.index('CONSTITUTION')] == 'general':
                Sport_std+=(65-Sport_Avg)**2/txtData.shape[0]
            elif txtData[i][title.index('CONSTITUTION')] == 'good':
                Sport_std+=(80-Sport_Avg)**2/txtData.shape[0]
            elif txtData[i][title.index('CONSTITUTION')] == 'excellent':
                Sport_std+=(90-Sport_Avg)**2/txtData.shape[0]

        for i in range(txtData.shape[0]):
            for j in range(title.index('C1'),title.index('C9')+1):
                if np.isnan(txtData[i][j]):
                    txtData[i][j] = Study_std[j]
        for i in range(txtData.shape[0]):
            if txtData[i][-1] not in dic:
                txtData[i][-1] = 'general'

        correletion = CalZ(txtData,title.index('C1'),title.index('C9'),Study_Avg,Study_std,Sport_std,Sport_std)
        return txtData,correletion

# 四舍五入对应的字典
dic_near = {'0':0,'1':0,'2':0,'3':1,'4':1,'5':1,'6':1,'7':1,'8':2,'9':2}


# 绘制散点图
def DrawScatter(txtData,a,b):
    x = []
    y = []
    for i in range(txtData.shape[0]):
        x.append(txtData[i][a])
        y.append(txtData[i][b])
    plt.scatter(x,y)
    plt.show()

# 绘制条形图
def DrawHist(txtData,a):
    x = []
    for i in range(txtData.shape[0]):
        if dic_near[str(int(txtData[i][a]%10))]==0:
            x.append(int(txtData[i][a]/10)*10)
        elif dic_near[str(int(txtData[i][a]%10))]==1:
            x.append(int(txtData[i][a]/10)*10+5)
        else:
            x.append((int(txtData[i][a]/10)+1)*10)
    plt.hist(x,histtype='bar', rwidth=0.8)
    plt.show()

# Z_SCORE标准化
def Z_Score(txtData):
    Study_Avg = CalMean(txtData,title.index('C1'),title.index('C10'))
    Study_Std = CalStd(txtData,title.index('C1'),title.index('C10'),Study_Avg)
    for i in range(len(Study_Std)):
        Study_Std[i] = math.sqrt(Study_Std[i])
    Sport_Avg = 0
    for i in range(txtData.shape[0]):
        if txtData[i][title.index('CONSTITUTION')] == 'bad':
            Sport_Avg += 50
        elif txtData[i][title.index('CONSTITUTION')] == 'general':
            Sport_Avg += 65
        elif txtData[i][title.index('CONSTITUTION')] == 'good':
            Sport_Avg += 80
        elif txtData[i][title.index('CONSTITUTION')] == 'excellent':
            Sport_Avg += 90

    Sport_Avg = Sport_Avg / txtData.shape[0]

    Sport_std = 0
    for i in range(txtData.shape[0]):
        if txtData[i][title.index('CONSTITUTION')] == 'bad':
            Sport_std += (50 - Sport_Avg) ** 2 / txtData.shape[0]
        elif txtData[i][title.index('CONSTITUTION')] == 'general':
            Sport_std += (65 - Sport_Avg) ** 2 / txtData.shape[0]
        elif txtData[i][title.index('CONSTITUTION')] == 'good':
            Sport_std += (80 - Sport_Avg) ** 2 / txtData.shape[0]
        elif txtData[i][title.index('CONSTITUTION')] == 'excellent':
            Sport_std += (90 - Sport_Avg) ** 2 / txtData.shape[0]
    Sport_std = math.sqrt(Sport_std)
    Z = []
    for i in range(txtData.shape[0]):
        for j in range(title.index('C1'),title.index('CONSTITUTION')+1):
            if txtData[i][j]=='bad':
                Z.append((50-Sport_Avg)/Sport_std)
                break
            if txtData[i][j]=='general':
                Z.append((65 - Sport_Avg) / Sport_std)
                break

            if txtData[i][j]=='good':
                Z.append((80 - Sport_Avg) / Sport_std)
                break

            if txtData[i][j]=='excellent':
                Z.append((90 - Sport_Avg) / Sport_std)
                break

            if np.isnan(txtData[i][j]):
                Z.append(0)
                continue
            Z.append((txtData[i][j]-Study_Avg[j-5])/Study_Std[j-5])
    Z = np.array(Z)
    Z = Z.reshape((txtData.shape[0],11))
    return Z

def CorretionMatrix(z):
    CorrMartix = np.zeros((z.shape[0],z.shape[0]))
    mean = []
    # 计算每一行Z_SCORE归一化矩阵的均值
    for i in range(z.shape[0]):
        x = 0
        for j in range(z.shape[1]):
            x+=z[i][j]
        mean.append((x/z.shape[1]))
    std = []
    # 计算每一行的方差
    for i in range(z.shape[0]):
        x = 0
        for j in range(z.shape[1]):
            x+=((z[i][j])-mean[i])**2
        std.append(x/(z.shape[1]-1))
    for i in range(z.shape[0]):

        for k in range(z.shape[0]):
            count = 0
            # if i==k:
            #     CorrMartix.append(1)
            #     continue
            for j in range(z.shape[1]):
                count+=(z[i][j]-mean[i])*(z[k][j]-mean[k])/(z.shape[1]-1)
            count = count/math.sqrt(std[i]*std[k])
            CorrMartix[i][k] = count
    return CorrMartix

if __name__=='__main__':
    # while(1):
    #     num = input("请根据要测试的选项输入对应的序号")
    # txtData,a = Caculate(txtData,4)
    # 处理缺失数据
    for i in range(txtData.shape[0]):
        if txtData[i][-1] not in dic:
            txtData[i][-1] = 'general'
        # if num==5:
        #     break
    # DrawScatter(txtData,title.index('C1'),title.index('CONSTITUTION'))
    # DrawHist(txtData,title.index('C1'))
    z = Z_Score(txtData)
    CorrMartix = CorretionMatrix(z)
    plt.subplots(figsize=(50, 50))
    sns.heatmap(data=CorrMartix,annot=True)
    plt.show()
    final = []
    count = 0
    for i in range(CorrMartix.shape[0]):
        final.append(CorrMartix[i].argsort()[-4:][::-1])
    final = np.delete(final,0,axis=1)
    np.savetxt('result.txt',final,fmt='%d')
    print(final)
    db_cur.close()
    db_conn.close()
