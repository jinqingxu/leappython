#author:Irene

import csv
import math
import os
# 3D point
class ThreeCorPoint:
    x=0
    y=0
    z=0
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

# 2D point
class TwoCorPoint:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y

# find the 3D cors for the 2D cors point on ipad
# the 2D cors are in pixels unit
def TwoCorToThreeCor(currentTwoCor):
    #the start point is the center of the ipad
    startThreeCor = ThreeCorPoint(-2.33, 44.395, -33.421)
    startTwoCor = TwoCorPoint(1024, 720)
    # * PixelToM change the unit from pixel to mm
    ChangeDis = math.sqrt(math.pow(startTwoCor.x - currentTwoCor.x, 2) + math.pow(startTwoCor.y - currentTwoCor.y, 2))*PixelToM
    ChangeX = abs(currentTwoCor.x - startTwoCor.x)*PixelToM # X's location change in 2D is the same as that in 3D
    Change2DY=abs(currentTwoCor.y-currentTwoCor.y)*PixelToM # Change2Y means the  location change of Y axis in the 2D plane
    ChangeY =  Change2DY* math.sin(Pi / 4) # the angle of the plane is 45 degree
    ChangZ =  Change2DY* math.cos(Pi / 4)
    # let the center point as base point, find the taget point's direction
    # right-up,left-up,left-down,right-down
    # right
    if currentTwoCor.x>startTwoCor.x:
        #right-up
        if currentTwoCor.y<startTwoCor.y:
            # x++ y++ z--
            newX=startThreeCor.x+ChangeX
            newY=startThreeCor.y+ChangeY
            newZ=startThreeCor.z-ChangZ
        #right-down
        else:
            # x++ y-- z++
            newX = startThreeCor.x + ChangeX
            newY = startThreeCor.y - ChangeY
            newZ = startThreeCor.z + ChangZ
    #left
    else:
        # left-up
        if currentTwoCor.y < startTwoCor.y:
            # x-- y++ z--
            newX = startThreeCor.x - ChangeX
            newY = startThreeCor.y + ChangeY
            newZ = startThreeCor.z - ChangZ
        # left-down
        else:
            # x-- y-- z++
            newX = startThreeCor.x - ChangeX
            newY = startThreeCor.y - ChangeY
            newZ = startThreeCor.z + ChangZ

    target=ThreeCorPoint(newX,newY,newZ)
    return target
