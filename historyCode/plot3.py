import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X=[]
Y=[]
Z=[]

# use points to draw the tablet planee
startX=-90
startY=0
startZ=-48
lengthX=90
# 45 * sqrt(2)
lengthY=32
changeX=0
changeY=0
step=0.5 # the density of the points in the plane
while changeX <lengthX:
    changeY=0
    while changeY<lengthY:
        X.append(startX+changeX)
        Y.append(startY+changeY)
        Z.append(startZ-changeY) # the angle is 45 degree, so the absolute change of Y and Z should be the same
        changeY+=step
    changeX+=step


ax.scatter(X, Y, Z,c='c', alpha=0.1,  marker='o', s = 1)
ax.set_xlabel('longitude')

ax.set_ylabel('latitude')

ax.set_zlabel('deepth')

plt.show()