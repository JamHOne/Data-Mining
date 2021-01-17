一、实验目的及要求
1. 掌握对基本机器学习概念的理解
2. 掌握分类和逻辑回归二分类实现的原理和方法
3. 按照既定格式书写实验报告
二、实验设备与平台
1. 实验设备：计算机；
2. 平台：Windows 10操作系统
三、实验内容
题目：学习sigmoid函数和逻辑回归算法。将实验三.2中的样例数据用聚类的结果打标签{0，1}，并用逻辑回归模型拟合。
1. 学习并画出sigmoid函数
2. 设计梯度下降算法，实现逻辑回归模型的学习过程。
3. 根据给定数据（实验三.2），用梯度下降算法进行数据拟合，并用学习好的模型对(2,6)分类。
实验实施：
（在此详述平台，技术栈，思路，处理逻辑等等）
logistic回归是一种广义线性回归（generalized linear model），因此与多重线性回归分析有很多相同之处。它们的模型形式基本上相同，都具有 w‘x+b，其中w和b是待求参数，其区别在于他们的因变量不同，多重线性回归直接将w‘x+b作为因变量，即y =w‘x+b，而logistic回归则通过函数L将w‘x+b对应一个隐状态p，p =L(w‘x+b),然后根据p 与1-p的大小决定因变量的值。如果L是logistic函数，就是logistic回归，如果L是多项式函数就是多项式回归。
本实验采用的逻辑回归函数为sigmoid函数，这个函数有一个特点，即x>0时可以认为1，x<0时可以认为-1，他是将概率反映为两个数值的一个函数，可用作二分类，本实验首先将教师给定的x,y点集进行聚类并打上标签，然后进行逻辑回归分析，此处省略打标签的函数，先画出sigmoid函数
1.	import numpy as np  
2.	import matplotlib.pyplot as plt  
3.	  
4.	def sigmoid(x):  
5.	    return 1/(1+np.exp(-x))  
6.	  
7.	t = np.linspace(-10,10,200)  
8.	y = []  
9.	for i in t:  
10.	    y.append(sigmoid(i))  
11.	plt.plot(t,y)  
12.	plt.show()  

有sigmoid函数后，将我们的点集x,y进行逻辑回归分析，分析过程如下：
首先假定有一个一维矩阵W = w0,w1,w2，其中要满足Z = WX有如下形式：w0+w1x+w2x，所以首先要给点集的第一列加上一个1作为常系数；而后定义损失函数，这里的损失函数用梯度下降法来进行标识，定义H = sigmoid(WX),即H = 1/(1+e^-XW),损失函数cost = -Y*log(H) – (1-Y)log(1-H),这里用错误分类的概率作为损失函数，错误分类的概率越低，则认为逻辑回归的W值越准确，求出cost函数的导数，并令导数为0，解得对应的函数解，更新W-=alpha*dC/dW,迭代到某个地方W的变化范围小于阙值，则认为逻辑回归已达到最优解
1.	def cal_W(xmat,ymat,alpha=0.0001,iterNum=10000):  
2.	    w = np.mat(np.random.randn(3,1))  
3.	    for _ in range(iterNum):  
4.	        h = sigmoid(xmat,w)  
5.	        dw = xmat.T*(h-ymat)  
6.	        w-=alpha*dw  
7.	    return w  
8.	w = cal_W(xmat,ymat)  
9.	w0 = w[0,0]  
10.	w1 = w[1,0]  
11.	w2 = w[2,0]  
12.	Xrange = np.arange(1,8,0.01)  
13.	Yrange = -w0/w2-w1/w2*Xrange  
14.	plt.plot(Xrange,Yrange,c='r')  
15.	plt.scatter(xmat[:,1][ymat==0].A,xmat[:,2][ymat==0].A,s=150)  
16.	plt.scatter(xmat[:,1][ymat==1].A,xmat[:,2][ymat==1].A,marker='^',s=150)  
17.	plt.show()  
这里省略了求导的过程，直接给出求导结果进行计算，所以具有特征性，不具有普遍性，如果换了一个回归函数，则不能用上述代码

3）分类2，6点只需要判断（2，6）在回归函数的上方还是下方即可


