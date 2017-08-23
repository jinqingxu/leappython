# -*- coding: UTF-8 -*-
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
N = 50 # 点的个数
x=[1,2,3]
y=[4,5,6]
colors = 'r' # 随机产生50个0~1之间的颜色值
# 画散点图
plt.scatter(x, y, c=colors, alpha=1,  marker='o' ,label='1', s = 30,edgecolors='white')
x2 = np.random.rand(N) * 2 # 随机产生50个0~2之间的x坐标
y2 = np.random.rand(N) * 2 # 随机产生50个0~2之间的y坐标
colors2= 'c' # 随机产生50个0~1之间的颜色值
plt.scatter(x2, y2, c=colors2, alpha=1,  marker='o' ,label='2', s = 70,edgecolors='white')
plt.xlabel('First Lift Up X(pixel)')
plt.ylabel('First Left Up Y(pixel')
plt.legend()
plt.grid(True)
plt.show()