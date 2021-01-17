# -*- coding = utf-8 -*-
# @time :  15:56
# @Author : Z~柳
# @File : 处理.py
# @Software : PyCharm
import pymysql.cursors
import copy
import math
from xlrd import open_workbook
import sys
def accountuser():
    # 创建一个连接对象，再使用创建游标
    con = pymysql.Connect(
        host='localhost',  # MySQL服务器地址
        port=3306,  # MySQL服务器端口号
        user='root',  # 用户名
        passwd='123456',  # 密码
        db='mysql',  # 数据库名称
        charset='utf8'  # 连接编码，存在中文的时候，连接需要添加charset='utf8'，否则中文显示乱码
    )
    cursor = con.cursor()

    # 执行SQL
    sql = 'select *from student'
    cursor.execute(sql)

    # 从游标中取出所有记录放到一个序列中并关闭游标
    result = cursor.fetchall()
    cursor.close()

    # 元祖类型result转换成列表类型b
    b = list(list([y for y in x]) for x in result)
    #result = list(result)
    return b
# 将两个list的性别类型转换成一致的
def trans_sex(a):
    #print(type(a))
    #print(a)
    for i in range(len(a)):
        if(a[i][3] == 'male'):
            a[i][3] = 'boy'
        elif(a[i][3] == 'female'):
            a[i][3] = 'girl'
   # return a
# 将两个list的身高转换成同一单位
def trans_Height(a):
    for i in range(len(a)):
        if(a[i][4] != ''and a[i][4] != 'Height'):
            a[i][4] = float(a[i][4])
            if(a[i][4] < 10):
                a[i][4] = a[i][4] * 100
            a[i][4] = int(a[i][4])
def trans_ID(a):
    for i in range(len(a)):
        if(a[i][0] != 'ID'):
            a[i][0] = int(a[i][0]) % 1000;
# 将两个数据源的数据处理成相同数据类型
# 处理数据库的数据
def run1():
    result = accountuser()
    trans_Height(result)
    #print(a)
   # print(type (result))
    trans_sex(result)
    trans_ID(result)
    return result
# 处理txt文本的数据
def run2():
    # 从
    fname = '数据源2-逗号间隔.txt'
    with open(fname, 'r+', encoding='utf-8') as f:
        s1 = [i[:-1].split(',') for i in f.readlines()]
    s = list(s1)
    #直接赋值,默认浅拷贝传递对象的引用而已,原始列表改变，被赋值的b也会做相同的改变
    #直接传s，函数中对a 修改同时修改了 s
    trans_sex(s)
    #深拷贝，包含对象里面的自对象的拷贝，所以原始对象的改变不会造成深拷贝里任何子元素的改变
    #函数对 a 修改不会对s 修改
    #trans_Height(copy.deepcopy(s))
    trans_Height(s)
    trans_ID(s)
    return s
# 将两张表数据源合成一张表，并且去除冗余和不一致性
def run(s1, s2):
    s3 = []
    for line in s1:
        for line2 in s2:
            if(line[0] == line2[0] and line[1] == line2[1] and line[2] == line2[2] and line[3] == line2[3]):
                if(len(s3) == 0 or s3[len(s3) - 1][0] != line[0] ):
                    if(line[0] != '' and line[1] != ''and line[2] != '' and line[3] != ''):
                        s3.append(line)
    return s3
# 清洗数据，填补缺失，缺失的用样本均值，男女分开求均值分开填补
def solve(s):
    sum =[[0,0] for i in range(16)]
    num = [[0,0] for i in range(16)]
    sex = ['boy','girl']
    Con = ['bad','general','good','excellent']
    for line in s:
        now = sex.index(line[3])
        for j in range(4, len(line)):
            k = line[j]
            if(j == len(line) - 1 and line[j] != ''):
                k = Con.index(line[j])
            if(line[j] != ''):
                sum[j][now] += int(k)
                num[j][now] += 1;
    for i in range(4, len(sum)):
        if(s[0][i] != ''):
            sum[i][0] = int(float(sum[i][0]) / num[i][0] + 0.5)
            sum[i][1] = int(float(sum[i][1])/ num[i][1] + 0.5)
    for i in range(0, len(s)):
        now = sex.index(s[i][3])
        for j in range(0, len(s[i])):
            if(s[i][j] == ''):
                if(j == len(s[i]) - 1):
                    s[i][j] = Con[sum[j][now]]
                elif (j == len(s[i]) - 2):
                    s[i][j] = 10
                else:
                    s[i][j] = int(sum[j][now])
# 学生中家乡在Beijing的所有课程的平均成绩, 返回百分制，保留整数
def ans1(list):
    num = 0
    sum = 0
    for line in list:
        if(line[2] == 'Beijing'):
            for i in range(5, 10):
                sum += int(line[i])
            for i in range(10,14):
                sum += int(line[i]) * 10
            num += 9
    return int(sum / num)
#学生中家乡在广州，课程1在80分以上，且课程10在9分以上的男同学的数量
def ans2(list):
    num = 0
    for line in list:
        if(line[3] == 'boy' and line[2] == 'Guangzhou' and int(line[5]) > 80 and line[14] > 9):
            num += 1
    return num
# 比较广州和上海两地女生的平均体能测试成绩，哪个地区的更强些？
def ans3(list):
    sex = ['boy', 'girl']
    Con = ['bad', 'general', 'good', 'excellent']
    fra = [25, 50, 75, 100]
    sum_G = 0
    sum_S = 0
    num_G = 0
    num_S = 0
    for line in list:
        if(line[3] == 'girl'):
            if(line[2] == 'Guangzhou'):
                sum_G += fra[Con.index(line[15])]
                num_G += 1
            elif(line[2] == 'Shanghai'):
                sum_S += fra[Con.index(line[15])]
                num_S += 1
    if(sum_G * num_S > sum_S * num_G):
        return 'Guangzhou'
    else:
        return 'Shanhai'

#学习成绩和体能测试成绩，两者的相关性是多少？
def ans4(list):
    sex = ['boy', 'girl']
    Con = ['bad', 'general', 'good', 'excellent']
    fra = [25, 50, 75, 100]
    # 求均值
    mean_s = [] #各科学习成绩均值
    mean_b = 0 #体侧成绩均值
    len_line = len(list)
    len_col = 10
    for i in range(5, 15):
        now = 0
        for line in list:
             now += int(line[i])
        now /= len_line
        mean_s.append(now)
    for line in list:
        mean_b += fra[Con.index(line[15])]
    mean_b /= len_line
    '''
    for i in range(0, 10):
        print(mean_s[i])
    '''
    # 求标准差
    var_s = [] #各科学习成绩方差
    var_b = 0 #体侧成绩标准差
    for i in range(5, 15):
        now = 0
        tmp = 1
        if(i >= 10):
            tmp = 10
        for line in list:
            now += tmp * tmp * (int(line[i]) - mean_s[i - 5]) * (int(line[i]) - mean_s[i - 5])
        var_s.append(math.sqrt(now/(len_line - 1)))
    for line in list:
        var_b += (fra[Con.index(line[15])] - mean_b) * (fra[Con.index(line[15])] - mean_b)
    var_b /= (len_line - 1)
    var_b = math.sqrt(var_b)
   # 求Z
    Z_s = []
    Z_b = []
    for i in range(5, 15):
        Z_s.append([])
        tmp = 1
        Z = 0
        if(i >= 10):
            tmp = 10
        for line in list:
            Z = tmp * float(line[i]) - mean_s[i - 5]
            if(var_s[i - 5] != 0):
                Z_s[i - 5].append(Z/float(var_s[i - 5]))

    for line in list:
        Z_b.append( (fra[Con.index(line[15])] - mean_b)/var_b)

    for i in range(0, 10):
        print("C",end="")
        print(i + 1,end="")
        print("成绩与体侧成绩的相关性为:")
        Z = 0
        for j in range(0, len(Z_s[i])):
            Z += Z_s[i][j] * Z_b[j]
        print(Z)

#主函数
if __name__ == '__main__':
    # 将两个数据源的数据类型转换成一致的
    sourse1 = run1()
    sourse2 = run2()
    # 将两张表数据源合成一张表，并且去除冗余的
    result = run(copy.deepcopy(sourse1), copy.deepcopy(sourse2))
    # 清洗数据，填补缺失，缺失的用样本均值，男女分开求均值分开填补，C10数据源中没有数据，因而全部填补为10分
    solve(result)

    # 问题一：学生中家乡在Beijing的所有课程的平均成绩, 返回百分制，保留整数
    print("问题一：",ans1(copy.deepcopy(result)))
    # 学生中家乡在广州，课程1在80分以上，且课程10在9分以上的男同学的数量
    print("问题二：",ans2(copy.deepcopy(result)))
    # 比较广州和上海两地女生的平均体能测试成绩，哪个地区的更强些？
    print("问题三：",ans3(copy.deepcopy(result)))
    # 学习成绩和体能测试成绩，两者的相关性是多少？
    print("问题四：")
    ans4(copy.deepcopy(result))
