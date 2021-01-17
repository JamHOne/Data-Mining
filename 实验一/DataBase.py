# -*- coding = utf-8 -*-
# @time :  14:09
# @Author : Z~柳
# @File : mys.py
# @Software : PyCharm
import pymysql.cursors
from xlrd import open_workbook
import sys
# excel文件
# 第一步打开excel文件，类似普通的文件open操作。注意open_workbook的参数必须是unicode编码
book = open_workbook('数据源.xlsx')

# 表格
# 一个excel文件中可能有多个表，可以通过sheets()方法返回关于所有表格的list列表
sheet = book.sheets()[0]	#通过下标可以获取某一个表格

# 下面获取一个表格内特定行的特定列的值
#sheet.cell_value(i,j)	#表格获取i行j列的值，一般会使用strip()去掉空格

# sheet有很多关于表格的属性
tolRows = sheet.nrows	#表格的总行数
columns = str(sheet.ncols)
print(columns)
# 连接数据库
connect = pymysql.Connect(
    host='localhost', # MySQL服务器地址
    port=3306, #MySQL服务器端口号
    user='root', #用户名
    passwd='123456', #密码
    db='mysql',  # 数据库名称
    charset='utf8'  #连接编码，存在中文的时候，连接需要添加charset='utf8'，否则中文显示乱码
)

# 获取游标
cursor = connect.cursor()

# 建表
cursor.execute("create table Student(ID char(20),Name char(20),City char(20), Gender char(20), Height char(20), C1 char(20), C2 char(20), C3 char(20), C4 char(20), C5 char(20), C6 char(20), C7 char(20), C8 char(20), C9 char(20), C10 char(20), Constitution char(20))character set utf8;")

# 插入数据
sql = 'INSERT INTO STUDENT(ID, Name, City, Gender, Height, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10,Constitution) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
for r in range(1, tolRows):
    ID      = sheet.cell(r, 0).value
    Name    = sheet.cell(r, 1).value
    City    = sheet.cell(r, 2).value
    Gender = sheet.cell(r, 3).value
    Height = sheet.cell(r, 4).value
    C1 = sheet.cell(r, 5).value
    C2 = sheet.cell(r, 6).value
    C3 = sheet.cell(r, 7).value
    C4 = sheet.cell(r, 8).value
    C5 = sheet.cell(r, 9).value
    C6 = sheet.cell(r, 10).value
    C7 = sheet.cell(r, 11).value
    C8 = sheet.cell(r, 12).value
    C9 = sheet.cell(r, 13).value
    C10 = sheet.cell(r, 14).value
    Constitution = sheet.cell(r, 15).value
    VALUES = (ID, Name, City, Gender, Height, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10,Constitution)
    cursor.execute(sql, VALUES)
    connect.commit()
# 关闭连接
cursor.close()
connect.close()

