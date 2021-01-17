一、实验目的及要求
1. 掌握对基本机器学习概念的理解
2. 掌握聚类实现的原理和方法
3. 按照既定格式书写实验报告
二、实验设备与平台
1. 实验设备：计算机；
2. 平台：Windows 10操作系统
三、实验内容
题目：用C++实现k-means聚类算法，
1. 对实验二中的z-score归一化的成绩数据进行测试，观察聚类为2类，3类，4类，5类的结果，观察得出什么结论？
2. 由老师给出测试数据，进行测试，并画出可视化出散点图，类中心，类半径，并分析聚为几类合适。
现有样例(x,y)数据对，
x	3.45	1.76	4.29	3.35	3.17	3.68	2.11	2.58	3.45	6.17	4.2	5.87	5.47	5.97	6.24	6.89	5.38	5.13	7.26	6.32
y	7.08	7.24	9.55	6.65	6.41	5.99	4.08	7.1	7.88	5.4	6.46	3.87	2.21	3.62	3.06	2.41	2.32	2.73	4.19	3.62
找到聚类中心后，判断(2,6)是属于哪一类？
实验实施：
（在此详述平台，技术栈，思路，处理逻辑等等）
1）K-means的核心思想
KMeans算法的基本思想是初始随机给定K个簇中心，按照最邻近原则把待分类样本点分到各个簇。然后按平均法重新计算各个簇的质心，从而确定新的簇心。一直迭代，直到簇心的移动距离小于某个给定的值。
K-Means聚类算法主要分为三个步骤：
(1)第一步是为待聚类的点寻找聚类中心；
(2)第二步是计算每个点到聚类中心的距离，将每个点聚类到离该点最近的聚类中去；
(3)第三步是计算每个聚类中所有点的坐标平均值，并将这个平均值作为新的聚类中心；
反复执行(2)、(3)，直到聚类中心不再进行大范围移动或者聚类次数达到要求为止。
(a)未聚类的初始点集；
(b)随机选取两个点作为聚类中心；
(c)计算每个点到聚类中心的距离，并聚类到离该点最近的聚类中去；
(d)计算每个聚类中所有点的坐标平均值，并将这个平均值作为新的聚类中心；
(e)重复(c),计算每个点到聚类中心的距离，并聚类到离该点最近的聚类中去；
(f)重复(d),计算每个聚类中所有点的坐标平均值，并将这个平均值作为新的聚类中心。
代码如下:
1.	# 初始化最开始的聚类点  
2.	def random_initialize(dataset,k):  
3.	    centroids = np.zeros((k,dataset.shape[1]))  
4.	    for i in range(k):  
5.	        index = int(rd.uniform(0,dataset.shape[0]))  
6.	        centroids[i,:] = dataset[index,:]  
7.	    return centroids  
8.	  
9.	# 计算点到聚类点的距离  
10.	def CalDistance(dataset,centroids):  
11.	    distance = 0  
12.	    for i in range(len(dataset)):  
13.	        distance+=(dataset[i]-centroids[i])**2  
14.	    distance = math.sqrt(distance)  
15.	    return distance  
16.	  
17.	def K_Means(dataset,k):  
18.	    centroids = random_initialize(dataset,k)  
19.	    clusterAssment = np.zeros((dataset.shape[0],1))  
20.	    r = {}  
21.	    # 迭代标记  
22.	    Isbool = True  
23.	    while Isbool:  
24.	        Isbool = False  
25.	        for i in range(dataset.shape[0]):  
26.	            minDist = 10000  
27.	            minIndex = 0  
28.	            for j in range(k):  
29.	                distance = CalDistance(dataset[i],centroids[j])  
30.	                if distance<minDist:  
31.	                    minDist = distance  
32.	                    minIndex = j  
33.	            #   如果存在还没有优化到最佳的节点，则继续迭代  
34.	            if clusterAssment[i] != minIndex:  
35.	                Isbool = True  
36.	            clusterAssment[i] = minIndex  
37.	        for j in range(k):  
38.	            new = []  
39.	            for x in range(dataset.shape[0]):  
40.	                if clusterAssment[x]==j:  
41.	                    new.append(dataset[x])  
42.	            new = np.array(new)  
43.	            # 重新定义聚类点，取聚类后的结果的均值作为新的聚类点  
44.	            centroids[j,:] = np.mean(new,axis=0)  
45.	    clusterAssment = clusterAssment.astype(int)  
46.	    # 计算聚类半径  
47.	    for i in range(len(clusterAssment)):  
48.	        if clusterAssment[i][0] not in r:  
49.	            r[clusterAssment[i][0]] = CalDistance(dataset[i],centroids[clusterAssment[i][0]])  
50.	            continue  
51.	        if r[clusterAssment[i][0]]<CalDistance(dataset[i],centroids[clusterAssment[i][0]]):  
52.	            r[clusterAssment[i][0]] = CalDistance(dataset[i],centroids[clusterAssment[i][0]])  
53.	    return centroids,clusterAssment,r  

2)对实验二计算的z-score归一矩阵进行聚类
1.	for i in range(2, 6):  
2.	    centroids, clusterAssment, minDist = K_Means.K_Means(z, i)  
3.	    print(centroids)  

3）根据教师给出的点集进行聚类，并可视化，观察聚类结果
1.	train = pd.read_csv('test.txt')  
2.	    train[train == '_'] = np.nan  
3.	    train = train.dropna(axis=0,how='any')  
4.	    train = np.array(train)  
5.	    train = train.astype(float)  
6.	  
7.	    for i in range(2,6):  
8.	        centroids,clusterAssment,minDist = K_Means(train,i)  
9.	        showCluster(train,i,centroids=centroids,clusterAssment=clusterAssment,minDist=minDist)  


