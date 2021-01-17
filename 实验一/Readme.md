

一、实验目的及要求
1. 掌握对数据集成、清洗概念的理解
2. 掌握数据清洗，样本数据构建基础方法
3. 掌握基本的统计方法
4. 按照既定格式书写实验报告
二、实验设备与平台
1. 实验设备：计算机；
2. 平台：Windows 10操作系统
三、实验内容
题目：广州大学某班有同学100人，现要从两个数据源汇总学生数据。第一个数据源在数据库中，第二个数据源在txt文件中，两个数据源课程存在缺失、冗余和不一致性，请用C/C++/Java程序实现对两个数据源的一致性合并以及每个学生样本的数值量化。
数据库表：ID (int), 姓名(string), 家乡(string:限定为Beijing / Guangzhou / Shenzhen / Shanghai), 性别（string:boy/girl）、身高（float:单位是cm)）、课程1成绩（float）、课程2成绩（float）、...、课程10成绩(float)、体能测试成绩（string：bad/general/good/excellent）；其中课程1-课程5为百分制，课程6-课程10为十分制。
txt文件：ID(string：6位学号)，性别（string:male/female）、身高（string:单位是m)）、课程1成绩（string）、课程2成绩（string）、...、课程10成绩(string)、体能测试成绩（string：差/一般/良好/优秀）；其中课程1-课程5为百分制，课程6-课程10为十分制。
两个数据源合并后读入内存，并统计：
1. 学生中家乡在Beijing的所有课程的平均成绩。


2. 学生中家乡在广州，课程1在80分以上，且课程9在9分以上的男同学的数量。(备注：该处做了修正，课程10数据为空，更改为课程9)
3. 比较广州和上海两地女生的平均体能测试成绩，哪个地区的更强些？
4. 学习成绩和体能测试成绩，两者的相关性是多少？（九门课的成绩分别与体能成绩计算相关性）
实验实施：
（在此详述平台，技术栈，思路，处理逻辑等等）
Pycharm2020.3(anaconda3)
实验运用到了嵌入式sql语句的使用，在python中调用oracle语句，实现数据库的读写
1.	'''
2.	    连接数据库，账号名为cc，密码为Ccpassowrd，使用本地IP进行连接 
3.	    数据库名为TESTDATA，从中取出所有数据 
4.	'''  
5.	db_conn = cx_Oracle.connect("cc","oracle","localhost/orcl")  
6.	db_cur = db_conn.cursor()  
7.	result = db_cur.execute("select * from TESTDATA")  
读取数据库数据流后，还需要读取文件数据流，此处使用read_csv函数来进行读取
1.	txtData_set = pd.read_csv('data.txt',sep=',')  
2.	txtData = np.array(txtData_set)  

数据处理的步骤包括处理数据冗余，数据丢失，数据重复，单位一致化等等
1.	# 数据单位一致  
2.	for i in range(0,txtData.shape[1]):  
3.	    for j in range(0,txtData.shape[0]):  
4.	        if i == title.index('HEIGHT'):  
5.	            txtData[j][i] = txtData[j][i]*100  
6.	        if i == title.index('ID'):  
7.	            txtData[j][i] = txtData[j][i]%1000  
8.	        if i == title.index('GENDER'):  
9.	            if txtData[j][i] == 'male':  
10.	                txtData[j][i] = 'boy'  
11.	            if txtData[j][i] == 'female':  
12.	                txtData[j][i] = 'girl'  

1.	# 数据冗余处理  
2.	i = 0  
3.	while(i < txtData_row):  
4.	    if txtData[i][title.index('ID')] not in dataLabel:  
5.	        dataLabel[txtData[i][title.index('ID')]] = 0  
6.	    dataLabel[txtData[i][title.index('ID')]] += 1  
7.	    if dataLabel[txtData[i][title.index('ID')]] > 1:  
8.	        print("出现数据冗余,行数为%d" % (i))  
9.	        txtData = np.delete(txtData, i, 0)  
10.	        i -= 1  
11.	    txtData_row = txtData.shape[0]  
12.	    i += 1  

1.	# 数据缺失处理  
2.	while(i < txtData_row):  
3.	    num = i + 1  
4.	    if num != txtData[i][title.index('ID')]:  
5.	        # print(num)  
6.	        arr = db_cur.execute(  
7.	            'select * from TESTDATA where ID = %s and rownum<2' %  
8.	            num)  
9.	        testData = []  
10.	        for re in arr:  
11.	            re = list(re)  
12.	            testData.append(re)  
13.	        testData = np.array(testData)  
14.	        testData = testData.flatten()  
15.	        if testData.shape == ():  
16.	            # txtData = np.append(txtData,testData, axis=2)  
17.	            txtData = np.row_stack((txtData, testData))  
18.	    txtData_row = txtData.shape[0]  
19.	    i += 1  

1.	# 数据重复处理  
2.	while(i < txtData_row):  
3.	    if txtData[i][title.index('ID')] not in dataLabel:  
4.	        dataLabel[txtData[i][title.index('ID')]] = 0  
5.	    dataLabel[txtData[i][title.index('ID')]] += 1  
6.	    if dataLabel[txtData[i][title.index('ID')]] > 1:  
7.	        txtData = np.delete(txtData, i, 0)  
8.	        i -= 1  
9.	    txtData_row = txtData.shape[0]  
10.	    i += 1  
定义一个字典，存放不同体测成绩对应的数值
1.	dic = {'bad': 50, 'general': 65, 'good': 80, 'excellent': 90}  

数据处理过后，根据题目要求对数据进行处理
5. 学生中家乡在Beijing的所有课程的平均成绩。
6. for i in range(txtData.shape[0]):  
7.     sum = 0  
8.     if txtData[i][title.index('CITY')]:  
9.         for j in range(title.index('C1'), title.index('C9') + 1):  
10.             if j == 5 or j == 6 or j == 7 or j == 8 or j == 9 or j == 10:  
11.                 sum += txtData[i][j] * 10  
12.                 break  
13.             sum += txtData[i][j]  
14.     avg = sum / 10  
15.     Beijing_avgGrade[txtData[i][title.index('NAME')]] = avg  
16. return Beijing_avgGrade  

学生中家乡在广州，课程1在80分以上，且课程9在9分以上的男同学的数量。(备注：该处做了修正，课程10数据为空，更改为课程9)
1.	counter = 0  
2.	        for i in range(txtData.shape[0]):  
3.	            if txtData[i][title.index('CITY')] == 'Guangzhou' and txtData[i][title.index(  
4.	                    'C1')] >= 80 and txtData[i][title.index('C9')] >= 6 and txtData[i][title.index('GENDER')] == 'boy':  
5.	                counter += 1  
6.	        return counter  

比较广州和上海两地女生的平均体能测试成绩，哪个地区的更强些？
1.	GuangzhouList = []  
2.	        ShanghaiList = []  
3.	        GuangzhouSum = 0  
4.	        ShanghaiSum = 0  
5.	        for i in range(txtData.shape[0]):  
6.	            if txtData[i][title.index('CITY')] == 'Guangzhou':  
7.	                GuangzhouList.append(txtData[i][title.index('CONSTITUTION')])  
8.	            elif(txtData[i][title.index('CITY')]) == 'Shanghai':  
9.	                ShanghaiList.append(txtData[i][title.index('CONSTITUTION')])  
10.	        for item in GuangzhouList:  
11.	            if item == 'bad':  
12.	                GuangzhouSum += 50  
13.	            elif(item == 'general'):  
14.	                GuangzhouSum += 65  
15.	            elif(item == 'good'):  
16.	                GuangzhouSum += 80  
17.	            elif(item == 'excellent'):  
18.	                GuangzhouSum += 90  
19.	        for item in ShanghaiList:  
20.	            if item == 'bad':  
21.	                ShanghaiSum += 50  
22.	            elif (item == 'general'):  
23.	                ShanghaiSum += 65  
24.	            elif (item == 'good'):  
25.	                ShanghaiSum += 80  
26.	            elif (item == 'excellent'):  
27.	                ShanghaiSum += 90  
28.	        Avg = {  
29.	            'Guangzhou': GuangzhouSum / len(GuangzhouList),  
30.	            'Shanghai': ShanghaiSum / len(ShanghaiList)}  
31.	        Avg = sorted(Avg.items(), reverse=False)  
32.	        return Avg[0][0]  

学习成绩和体能测试成绩，两者的相关性是多少？（九门课的成绩分别与体能成绩计算相关性）
均值公式	 
协方差公式	 
z-score规范化	 
数组A和数组B的相关性	 
这里A=[a1, a2,...ak,..., an],
B=[b1, b2,...bk,..., bn],
mean(A)代表A中元素的平均值
std是标准差，即对协方差的开平方。
点乘的定义： 
1.	# 计算均值  
2.	def CalMean(txtData, a, b):  
3.	    Study_Avg = []  
4.	    countNan = 0  
5.	    for i in range(a, b + 1):  
6.	        a = 0  
7.	        for j in range(txtData.shape[0]):  
8.	            if np.isnan(txtData[j][i]):  
9.	                countNan += 1  
10.	                continue  
11.	            a += txtData[j][i]  
12.	        a = a / (txtData.shape[0] - countNan)  
13.	        Study_Avg.append(a)  
14.	    return Study_Avg  

1.	# 计算方差  
2.	def CalStd(txtData, a, b, mean):  
3.	    countNan = 0  
4.	    Study_std = []  
5.	    for i in range(a, b + 1):  
6.	        grade = 0  
7.	        for j in range(txtData.shape[0]):  
8.	            if np.isnan(txtData[j][i]):  
9.	                countNan += 1  
10.	                continue  
11.	            grade += (txtData[j][i] - mean[i - 5]) ** 2 / \  
12.	                (txtData.shape[0] - 1 - countNan)  
13.	        Study_std.append(grade)  
14.	    return Study_std  

1.	# 计算相关系数  
2.	def CalZ(txtData, a, b, StudyMean, StudyStd, SportMean, SportStd):  
3.	    correletion = []  
4.	    z_score = 0  
5.	    for i in range(a, b + 1):  
6.	        for j in range(txtData.shape[0]):  
7.	            if np.isnan(txtData[j][i]):  
8.	                z = (txtData[j - 1][i] - StudyMean[i - 5]) / math.sqrt(  
9.	                    StudyStd[i - 5]) * (dic[txtData[j][-1]] - SportMean) / SportStd  
10.	                continue  
11.	            if txtData[j][-1] not in dic:  
12.	                continue  
13.	            z = (txtData[j][i] - StudyMean[i - 5]) / math.sqrt(StudyStd[i - 5]  
14.	                                                               ) * (dic[txtData[j][-1]] - SportMean) / SportStd  
15.	        z_score += z  
16.	        correletion.append(z_score)  
17.	    return correletion  

1.	z = 0  
2.	        countNan = 0  
3.	        Sport_Avg = 0  
4.	        Study_std = []  
5.	        Sport_std = 0  
6.	        z_score = 0  
7.	        correletion = []  
8.	  
9.	        Study_Avg = CalMean(txtData, title.index('C1'), title.index('C9'))  
10.	  
11.	        for i in range(txtData.shape[0]):  
12.	            if txtData[i][title.index('CONSTITUTION')] == 'bad':  
13.	                Sport_Avg += 50  
14.	            elif txtData[i][title.index('CONSTITUTION')] == 'general':  
15.	                Sport_Avg += 65  
16.	            elif txtData[i][title.index('CONSTITUTION')] == 'good':  
17.	                Sport_Avg += 80  
18.	            elif txtData[i][title.index('CONSTITUTION')] == 'excellent':  
19.	                Sport_Avg += 90  
20.	  
21.	        Sport_Avg = Sport_Avg / txtData.shape[0]  
22.	  
23.	        Study_std = CalStd(  
24.	            txtData,  
25.	            title.index('C1'),  
26.	            title.index('C9'),  
27.	            Study_Avg)  
28.	        for i in range(txtData.shape[0]):  
29.	            if txtData[i][title.index('CONSTITUTION')] == 'bad':  
30.	                Sport_std += (50 - Sport_Avg)**2 / txtData.shape[0]  
31.	            elif txtData[i][title.index('CONSTITUTION')] == 'general':  
32.	                Sport_std += (65 - Sport_Avg)**2 / txtData.shape[0]  
33.	            elif txtData[i][title.index('CONSTITUTION')] == 'good':  
34.	                Sport_std += (80 - Sport_Avg)**2 / txtData.shape[0]  
35.	            elif txtData[i][title.index('CONSTITUTION')] == 'excellent':  
36.	                Sport_std += (90 - Sport_Avg)**2 / txtData.shape[0]  
37.	  
38.	        for i in range(txtData.shape[0]):  
39.	            for j in range(title.index('C1'), title.index('C9') + 1):  
40.	                if np.isnan(txtData[i][j]):  
41.	                    txtData[i][j] = Study_std[j]  
42.	        for i in range(txtData.shape[0]):  
43.	            if txtData[i][-1] not in dic:  
44.	                txtData[i][-1] = 'general'  
45.	  
46.	        correletion = CalZ(  
47.	            txtData,  
48.	            title.index('C1'),  
49.	            title.index('C9'),  
50.	            Study_Avg,  
51.	            Study_std,  
52.	            Sport_std,  
53.	            Sport_std)  


