import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X=[]
Y=[]
Z=[]
i=0
while i <1:
    X.append(i)
    Y.append(i)
    Z.append(i)
    i=i+0.001

ax.scatter(X, Y, Z,c='c', alpha=0.1,  marker='o', s = 1)
ax.set_xlabel('longitude')

ax.set_ylabel('latitude')

ax.set_zlabel('deepth')

plt.show()