#author:Irene

import csv
import math
from GlobalVariables import Pi
from GlobalVariables import PixelToM
from GlobalVariables import TwoCorPoint
from GlobalVariables import ThreeCorPoint
from GlobalVariables import  startTwoCor
from GlobalVariables import  startThreeCor
from GlobalVariables import path
from GlobalVariables import offsetAndroidBlock
from GlobalVariables import offsetAndroidTrial
from GlobalVariables import offsetAndroidTargetX
from GlobalVariables import offsetAndroidTargetY


# find the Relative X and Y cors for point on the ipad
# let the target point be the center point
# the X axis be the target line
# the Y axis be the line vertical to the target line
# let l be the line passing start(center) point and current point
# first calculate len(l)
# then calcultate the intersaction angle of l and x-axis,let it be a
# cos(a)=(a.b)/(|a||b|)
# then the new x is startX+/-len(l)*cos(a)
# the new y is startY+/-len(l)*sin(a)
# then we need to judge which quadrant the current point is
# so that we can decide + or - in x or y axis
def getRelativeXandY(curX,curY,curZ,startX,startY,startZ,targetX,targetY,targetZ):
    lengthl=calculate_3D_Dis_Of_Two_Points(curX,curY,curZ,targetX,targetY,targetZ) # the length of the l vector
    lengthx=calculate_3D_Dis_Of_Two_Points(startX,startY,startZ,targetX,targetY,targetZ) # the length of the x axis vector
    # the direction vector of X axis is (startX-targetX,startY-targetY,startZ-targetZ)
    # the direction vector of l axis is (curX-targetX,curY-targetY,curZ-targetZ)
    # cos(a)=(a.b)/(|a||b|)
    cosa=((startX-targetX)*(curX-targetX)+(startY-targetY)*(curY-targetY)+(startZ-targetZ)*(curZ-targetZ))/(lengthl*lengthx)
    # the direction vector of Y axis is vertical to (0,1,1)
    # the direction vector of Y axis is vertical to (startX-targetX,startY-targetY,startZ-targetZ)
    # the direction vector of Y axis is (startY-targetY-startZ+targetZ,targetX-startZ,startX-targetX)
    diffX=lengthl*cosa
    sina=math.sqrt(1-pow(cosa,2))
    diffY=lengthl*sina
    if curY>targetY: # above the line
        if curX>targetX: # be right to the center point
            # x++
            # y++
            newX=targetX+diffX
            newY=targetY+diffY
        else: # be left to the center point
            # x--
            # y++
            newX=targetX-diffX
            newY=targetY+diffY
    else: # beneath the line
        if curX>targetX: # be right to the center point
            # x++
            # y--
            newX=targetX+diffX
            newY=targetY-diffY
        else: # be left to the center point
            # x--
            # y--
            newX=targetX-diffX
            newY=targetY-diffY
    return newX,newY

# input pid,block,trial
# find the 3D position for a target
def getTargetLocationFor3D(pid,block,trial):
    file = path + "PId_" + str(pid) + "_TwoDFittsData_External.csv"
    with open(file) as f:
        f_csv = csv.reader(f)
        for i in range(0, 10):  # skip the beginning
            next(f_csv)
        for row in f_csv:
            if str(row[offsetAndroidBlock])==str(block) and str(row[offsetAndroidTrial])==str(trial):
                targetX=float(row[offsetAndroidTargetX])
                targetY=float(row[offsetAndroidTargetY])
                targetTwoCor=TwoCorPoint(targetX,targetY) # the target point in 2D world
                targetThreeCor=TwoCorToThreeCor(targetTwoCor)
                return targetThreeCor
    return -1 # not found



# calculate the exact 3D position of targets
# we keep the finger on the start button
# then we get the average value of the start position
# find the 3D cors for the 2D cors point on ipad
# the 2D cors are in pixels unit
def TwoCorToThreeCor(currentTwoCor):
    # the start point is the center of the ipad
    # PixelToM change the unit from pixel to mm
    ChangeX = abs(currentTwoCor.x - startTwoCor.x)*PixelToM # X's location change in 2D is the same as that in 3D
    Change2DY=abs(currentTwoCor.y-startTwoCor.y)*PixelToM # Change2Y means the  location change of Y axis in the 2D plane
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

    target=ThreeCorPoint(round(newX),round(newY,0),round(newZ,0))
    return target




# this function is not used yet
# in 2D cors
# judge whether a point is above or beneath to a line
# cur is the point
# start and end is two points in the line
# the function of the line is x-startX/endX-startX=y-startY/endY-startY
# then y=starty+(endY-startY)*(x-startX)/(endX-startX)
# put the value of curX into the function,output a calY
# if calY<curY
# the point is above the line
# if calY>curY
# the point is beneath the line
def judge2DPointAboveLine(curX,curY,startX,startY,endX,endY):
    calY=startY+(endY-startY)*(curX-startX)/(endX-startX)
    if calY<curY:
        return True
    else:
        return False

# this function is not used yet
# in a self-defined coordinate system,judge which quadrant is the cur point in
# (centerX,centerY) represents the center point
# (axisX1,axisY1) represents the point in the x axis
# (axisX2,axisY2) represents the point in the y axis
def judgeQuadrant(curX,curY,centerX,centerY,axisX1,axisY1,axisX2,axisY2):
    if judge2DPointAboveLine(curX,curY,centerX,centerY,axisX1,axisY1)==True: # above x
        if judge2DPointAboveLine(curX,curY,centerX,centerY,axisX2,axisY2)==True: # above y
            # the first quadrant
            return 1
        else: # beneath y
            return 2
    else: # beneath x
        if judge2DPointAboveLine(curX, curY, centerX, centerY, axisX2, axisY2) == True:  # above y
            # the first quadrant
            return 4
        else:  # beneath y
            return 3

# get the intersaction angle of two lines
# (x1,y1) (x2,y2) are the points on l1
# (x3,y3) (x4,y4) are the points on l2
# return sinA,cosA
def getIntersactionAngleOfTwoLines(X1,Y1,X2,Y2,X3,Y3,X4,Y4):
    k1=(Y2-Y1)/(X2-X1+0.0)
    k2=(Y4-Y3)/(X4-X3+0.0)
    tanA=abs((k2-k1)/(1+k1*k2))
    cosA=1/math.sqrt(pow(tanA,2)+1)
    sinA=tanA*cosA
    return sinA,cosA


# calculate the distance of two 3D points
def calculate_3D_Dis_Of_Two_Points(x1,y1,z1,x2,y2,z2):
    return math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2)+math.pow(z1-z2,2))

# get th intersaction point of a line and a plane
# let the line passing through curX,curY,curZ be l
# this function calculate the intersaction point of l and the ipad
# targetX targetY,targetZ is a point on the plane of ipad
# since the angle of the ipad is 45 degree,the normal vector of the ipad plane is (0,1,1)
# so the function of line l is (x-curX)/0=(y-curY)/1=(z-curZ)/1 ,that is y-curY=z-curZ=k
# let y=curY+k,z=curZ+k
# the function of the ipad is 0*(x-targetX)+1*(y-targetY)+1*(z-targetZ)=0
# put y and z into the ipad function
# k=(targetY+targetZ-curY-curZ)/2
# so y=curY+k=(targetY+targetZ+curY-curZ)/2
# z=curZ+k=(targetY+targetZ+curZ-curY)/2
# x=curX
def getIntersactionPointOfLineAndPlane(curX,curY,curZ,targetX,targetY,targetZ):
    return curX,(targetY + targetZ + curY - curZ) / 2,(targetY + targetZ + curZ - curY) / 2

# get the distance from a point to a line
def getDistanceOfPointAndLine(x1,y1,z1,x2,y2,z2,x,y,z):
    distanceLine = calculate_3D_Dis_Of_Two_Points(x1, y1, z1, x2, y2, z2)
    pow1 = math.pow((x1 - x) * (y2 - y1) - (y1 - y) * (x2 - x1), 2)
    pow2 = math.pow((y1 - y) * (z2 - z1) - (z1 - z) * (y2 - y1), 2)
    pow3 = math.pow((z1 - z) * (x2 - x1) - (x1 - x) * (z2 - z1), 2)
    distancePoint = math.sqrt(
        pow1 + pow2 + pow3) / distanceLine  # the area of the parallelogram divided by the length of the edge is the distance of a point to a line in 3D cors
    return distancePoint









