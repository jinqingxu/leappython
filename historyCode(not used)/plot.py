# -*- coding: UTF-8 -*-
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
'''
N = 50 # 点的个数
x=[1,2,3]
y=[4,5,6]
colors = 'r' # 随机产生50个0~1之间的颜色值
# 画散点图
plt.scatter(x, y, c=colors, alpha=1,  marker='o' ,label='1', s = 30,edgecolors='white')
x2 = np.random.rand(N) * 2 # 随机产生50个0~2之间的x坐标
y2 = np.random.rand(N) * 2 # 随机产生50个0~2之间的y坐标
z2=np.random.rand(N) * 2
colors2= 'c' # 随机产生50个0~1之间的颜色值

plt.scatter(x2,y2,z2, c=colors2, alpha=1,  marker='o', s = 70)
plt.xlabel('First Lift Up X(pixel)')
plt.ylabel('First Lift Up Y(pixel')
plt.zlabel('First Lift Up X(pixel)')
plt.legend()
plt.grid(True)
plt.show()
'''


class we:

    a=0
    b=0
    c=0

    def __eq__(self, other):

        return self.a==other.a and self.b==other.b and self.c==other.c

    def __init__(self,a,b,c):

        self.a=a
        self.b=b
        self.c=c

q1=we(1,1,1)
q2=we(1,1,1)
if q1== q2:
    print "ok"