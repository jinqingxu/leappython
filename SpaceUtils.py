# author:Irene
# functions in this script are helper functions in 3D calculation
# already add comments

import csv
import math

from GlobalVariables import *
'''
# this function is not used any more
# find the Relative X and Y cors for point on the tablet
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
'''

# input pid,block,trial
# find the 3D position for a target

def getTargetLocationFor3D(pid,block,trial,path):

    file = path + "PId_" + str(pid) + "_TwoDFittsData_External.csv"

    with open(file) as f:

        f_csv = csv.reader(f)
        for i in range(0, 9):  # skip the beginning
            next(f_csv)

        for row in f_csv:

            if str(row[colNumAndroidBlock])==str(block) and str(row[colNumAndroidTrial])==str(trial): # find the exact row of the trial

                targetX=float(row[colNumAndroidTargetX]) # the 2D targetX
                targetY=float(row[colNumAndroidTargetY]) # the 2D targetY
                targetTwoCor=TwoCorPoint(targetX,targetY) # the target point in 2D world
                targetThreeCor=TwoCorToThreeCor(targetTwoCor) # the target point in 3D world,with x,y,z
                return targetThreeCor

    return -1 # fail to find the trial

# use direction and amplitude as input
def getTargetLocationFor3DWithDirection(direction,amplitude):

    abschangeX=abs(math.cos(direction/180.0*Pi)*amplitude) # the absolute change of X is amplitude multiply with cos(angle)
    change2DY=abs(math.sin(direction/180.0*Pi)*amplitude) # change of Y in the 2D system is amplitude multiply with sin(angle)
    abschangeY=abs(change2DY*math.sin(tabletAngle/180.0*Pi)) # the absolute change of Y is change2DY multiply with sin(angle of tablet)
    abschangeZ=abs(change2DY*math.cos(tabletAngle/180.0*Pi)) # thea absolute change of Z is change2DZ multiply with cos(angle of tablet)

    if direction>=0 and direction<90: # right up
        changeX=abschangeX
        changeY=abschangeY
        changeZ=(-1)*abschangeZ

    if direction>=90 and direction<180: # left up
        changeX=(-1)*abschangeX
        changeY=abschangeY
        changeZ=(-1)*abschangeZ

    if direction>=180 and direction<270: # left down
        changeX=(-1)*abschangeX
        changeY=(-1)*abschangeY
        changeZ=abschangeZ

    if direction>=270 and direction<=360: # right down
        changeX=abschangeX
        changeY=(-1)*abschangeY
        changeZ=abschangeZ


    # the target point

    newX=startThreeCor.x+changeX
    newY=startThreeCor.y+changeY
    newZ=startThreeCor.z+changeZ

    return ThreeCorPoint(newX,newY,newZ)

# input a point in 3D
# output the position in the projected plane

def LocationInProjectedPlane(oldThreeCor):
    # project the point in a new system that the y is the y axis in the 2D system on the tablet,the z is vertical to the tablet
    # in a word, in the new system, our tablet is vertical to the ground now
    newX=oldThreeCor.x # there is no change on X
    newY=oldThreeCor.y/math.sin(tabletAngle/180.0*Pi)
    newZ=oldThreeCor.z/math.sin(tabletAngle/180.0*Pi)
    return ThreeCorPoint(newX,newY,newZ)





# calculate the exact 3D position of targets
# we keep the finger on the start button
# then we get the average value of the start button position
# return the 3D cors for the 2D cors point on the tablet
# the 2D cors are in pixels unit

def TwoCorToThreeCor(currentTwoCor):

    # the start point is the center of the tablet
    # PixelToM change the unit from pixel to mm

    ChangeX = abs(currentTwoCor.x - startTwoCor.x)*PixelToM # X's location change in 2D is the same as that in 3D since the tablet is facing the leap motion
    Change2DY=abs(currentTwoCor.y-startTwoCor.y)*PixelToM # Change2Y means the  location change of Y axis in the 2D system
    ChangeY =  Change2DY* math.sin(Pi* tabletAngle/(180+0.0)) # suppose the angle of the plane is x degree,the change of Y axis in the 3D system should be chang2DY multiplied by sin(Pi*x/180)
    ChangZ =  Change2DY* math.cos(Pi*tabletAngle/(180+0.0)) # the change of Z is  change2DY multiplied by cos(45)

    # find the target point's direction relative to the center point
    # there are four situati ons: right-up,left-up,left-down,right-down

    # right
    if currentTwoCor.x>startTwoCor.x:
        #right-up
        if currentTwoCor.y<startTwoCor.y:
            # in the leap motion system,the right up direction means increase in x and y,decrease in z
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



'''
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
'''

# get the intersaction angle of two lines l1 and l2
# (x1,y1) (x2,y2) are the points on l1
# (x3,y3) (x4,y4) are the points on l2
# return sinA,cosA
def getIntersactionAngleOfTwoLines(X1,Y1,X2,Y2,X3,Y3,X4,Y4):

    k1=(Y2-Y1)/(X2-X1+0.0) # the slope of l1
    k2=(Y4-Y3)/(X4-X3+0.0) # the slope of l2

    tanA=abs((k2-k1)/(1+k1*k2)) # tan(angle)
    cosA=1/math.sqrt(pow(tanA,2)+1)
    sinA=tanA*cosA

    return sinA,cosA


# calculate the distance of two 3D points
def calculate_3D_Dis_Of_Two_Points(x1,y1,z1,x2,y2,z2):
    return math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2)+math.pow(z1-z2,2))

'''
# this function is not used any time
# originally used in LeapAnalyzerOriginal
# let the line vertical to the plane and  passing through curX,curY,curZ  be l
# this function calculate the intersaction point of l and the tablet plane
# targetX targetY,targetZ is a point on the tablet plane
# since the angle of the tablet plane is 45 degree,the normal vector of the tablet plane is (0,1,1)
# so the function of line l is (x-curX)/0=(y-curY)/1=(z-curZ)/1 ,that is y-curY=z-curZ=k
# let y=curY+k,z=curZ+k
# the function of the tablet plane is 0*(x-targetX)+1*(y-targetY)+1*(z-targetZ)=0
# put y and z into the plane function
# k=(targetY+targetZ-curY-curZ)/2
# so y=curY+k=(targetY+targetZ+curY-curZ)/2
# z=curZ+k=(targetY+targetZ+curZ-curY)/2
# x=curX
def getIntersactionPointOfFingerAndTabletPlane(curX,curY,curZ,targetX,targetY,targetZ):
    return curX,(targetY + targetZ + curY - curZ) / 2,(targetY + targetZ + curZ - curY) / 2
'''


# let the line vertical to the plane and  passing through curX,curY,curZ  be l
# this function calculate the intersaction point of l and the plane
# (planeX,planeY,planeZ) is a point on the  plane
# (nx,ny,nz) is the normal vector of the plane
# the plane function is nx*(x-planeX)+ny*(y-planeY)+nz*(z-planeZ)=0 (1)
# since l is vertical to the plane
# (nx,ny,nz) is the direction vector of l
# so the function of l is (x-curX)/nx=(y-curY)/ny=(z-curZ)/nz=k
# thus x=k*nx+curX y=k*ny+curY z=k*nz+curZ
# put x,y,z into equation (1)
# k=(-nx*curX+nx*planeX-ny*curY+ny*planeY-nz*curZ+nz*planeZ)/((nx)^2+(ny)^2+(nz)^2)
def getIntersactionPointOfPointAndPlane(curX,curY,curZ,planeX,planeY,planeZ,nx,ny,nz):
    k=(-nx*curX+nx*planeX-ny*curY+ny*planeY-nz*curZ+nz*planeZ)/((nx)^2+(ny)^2+(nz)^2)
    intersactionX=k*nx+curX
    intersactionY=k*ny+curY
    intersactionZ=k*nz+curZ
    return intersactionX,intersactionY,intersactionZ


# it is used in the movement error calculation
# this function is used to calculate the distance between a point and a plane
# (curX,curY,curZ) is the current point
# (planeX,planeY,planeZ) is a point on the  plane
# (nx,ny,nz) is the normal vector of the plane
def getDistanceBetweenPointAndPlane(curX,curY,curZ,planeX,planeY,planeZ,nx,ny,nz):
    # let the line vertical to the plane and  passing through curX,curY,curZ  be l
    # this function calculate the intersaction point of l and the plane
    intersactionX, intersactionY, intersactionZ=getIntersactionPointOfPointAndPlane(curX,curY,curZ,planeX,planeY,planeZ,nx,ny,nz)
    # the distance between a point and the plane is actually the distance between the point and the intersaction point
    dis=calculate_3D_Dis_Of_Two_Points(curX,curY,curZ,intersactionX,intersactionY,intersactionZ)
    return dis

'''
# this function is not used any more
# this function is used to calculate MO previously,but that's wrong
# it is replace by the function of getDistanceBetweenPointAndPlane
# get the distance from a point to a line in a 3D system
# used to calculate movement error in Mackenzie's measurement
def getDistanceOfPointAndLine(x1,y1,z1,x2,y2,z2,x,y,z):
    distanceLine = calculate_3D_Dis_Of_Two_Points(x1, y1, z1, x2, y2, z2)
    pow1 = math.pow((x1 - x) * (y2 - y1) - (y1 - y) * (x2 - x1), 2)
    pow2 = math.pow((y1 - y) * (z2 - z1) - (z1 - z) * (y2 - y1), 2)
    pow3 = math.pow((z1 - z) * (x2 - x1) - (x1 - x) * (z2 - z1), 2)
    distancePoint = math.sqrt(
        pow1 + pow2 + pow3) / distanceLine  # the area of the parallelogram divided by the length of the edge is the distance of a point to a line in 3D cors
    return distancePoint
'''









