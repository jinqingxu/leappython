# author:Irene
# seven measures from Mackenzie's paper
# already add comments

import csv
import math
from SpaceUtils import getDistanceBetweenPointAndPlane
from GlobalVariables import *



from SpaceUtils import getTargetLocationFor3D


class LeapAnalyzerMackenzie:
    pid=0
    block=0
    trial=0
    readFile=""
    frameArray=[]
    numberFrame=0
    movementDirectionChangeX=0
    movementDirectionChangeY=0
    movementDirectionChangeZ=0
    movementOffset=0
    movementError=0
    movementVaribility=0
    targetX=0
    targetY=0
    targetZ=0
    startX=0
    startY=0
    startZ=0
    taskAxisCrossing=0
    path=""

    def __init__(self,readFile,pid,block,trial,path):
        self.readFile=readFile
        self.pid=pid
        self.block=block
        self.trial=trial
        self.frameArray=[]
        self.numberFrame=0
        self.movementDirectionChangeX = 0
        self.movementDirectionChangeY = 0
        self.movementDirectionChangeZ = 0
        self.movementOffset = 0
        self.movementError = 0
        self.movementVaribility = 0
        self.path=path

    def loadLeapData(self):
        # load the split file
        self.frameArray=[]
        file = self.readFile # the split file
        with open(file) as f:
            f_csv = csv.reader(f)
            next(f_csv)
            for row in f_csv:
                self.frameArray.append(row)
        targetThreeCor = getTargetLocationFor3D(self.pid, self.block,self.trial,self.path)  # with accurate start coordinate in 3D,calculate the target 3D
        self.targetX = targetThreeCor.x
        self.targetY = targetThreeCor.y
        self.targetZ = targetThreeCor.z
        self.startX=startThreeCor.x
        self.startY=startThreeCor.y
        self.startZ=startThreeCor.z
        self.numberFrame=len(self.frameArray)

    def calculateNumberOfFrame(self):
        return self.numberFrame

    def calculateMovementDirectionChange(self):

        prevFrame = self.frameArray[0] # let the first frame be the initial prevFrame
        currentFrame = self.frameArray[1] # let the second frame be the initial currentFrame
        i = 2 # started from the third frame
        # the initial value
        prevDirectionX = "Right"
        prevDirectionY = "Up"
        prevDirectionZ = "Forward"
        currentDirectionX = ""
        currentDirectionY = ""
        currentDirectionZ = ""
        while i < len(self.frameArray):
            prevX = float(prevFrame[colNumSplitX])
            prevY = float(prevFrame[colNumSplitY])
            prevZ = float(prevFrame[colNumSplitZ])
            currentX = float(currentFrame[colNumSplitX])
            currentY = float(currentFrame[colNumSplitY])
            currentZ = float(currentFrame[colNumSplitZ])
            # update the self.movementDirectionChangX and return the current direction of X
            # if the same direction self.movementDirectionChangX++
            # else self.movementDirectionChangX--
            currentDirectionX = self.calculateMovementDirectionChangeX(prevX, currentX, prevDirectionX, currentDirectionX)
            currentDirectionY = self.calculateMovementDirectionChangeY(prevY, currentY, prevDirectionY, currentDirectionY) # update the self.movementDirectionChangY and return the current direction of Y
            currentDirectionZ = self.calculateMovementDirectionChangeZ(prevZ, currentZ, prevDirectionZ, currentDirectionZ) # update the self.movementDirectionChangZ and return the current direction of Z
            prevFrame = currentFrame # update the prevFrame be the current one
            currentFrame = self.frameArray[i] # update the current frame
            # replace the previous direction with the current one
            prevDirectionX = currentDirectionX
            prevDirectionY = currentDirectionY
            prevDirectionZ = currentDirectionZ
            i = i + 1

    def calculateMovementDirectionChangeX(self,prevX, currentX, prevDirectionX, currentDirectionX):
        if prevX != currentX:
            if currentX < prevX:
                currentDirectionX = "Left"
            else:
                currentDirectionX = "Right"
            if prevDirectionX != currentDirectionX:
                self.movementDirectionChangeX=self.movementDirectionChangeX+1
        return currentDirectionX

    def calculateMovementDirectionChangeY(self,prevY,currentY,prevDirectionY,currentDirectionY):
        if prevY != currentY:
            if currentY <prevY:
                currentDirectionY="Down"
            else:
                currentDirectionY="Up"
            if prevDirectionY!=currentDirectionY:
                self.movementDirectionChangeY=self.movementDirectionChangeY+1
        return currentDirectionY

    def calculateMovementDirectionChangeZ(self,prevZ,currentZ,prevDirectionZ,currentDirectionZ):
        if prevZ != currentZ:
            if currentZ < prevZ:
                currentDirectionZ = 'Backward'
            else:
                currentDirectionZ = 'Forward'
            if prevDirectionZ!=currentDirectionZ:
                self.movementDirectionChangeZ=self.movementDirectionChangeZ+1
        return currentDirectionZ

    # MV
    # the deviation of  movement error from the average value
    def calculateMovementVariability(self,movementOffset):
        sumMovementErrorDifference=0
        for i in range(0,len(self.frameArray)):
            currentFrame=self.frameArray[i]
            currentX=float(currentFrame[colNumSplitX])
            currentY=float(currentFrame[colNumSplitY])
            currentZ=float(currentFrame[colNumSplitZ])
            # the movement offset represent the average movement error
            differenceMovementErrorSqr=math.pow(self.calculateRealMovementError(self.startX,self.startY,self.startZ,self.targetX,self.targetY,self.targetZ,currentX,currentY,currentZ)-movementOffset,2)
            sumMovementErrorDifference=sumMovementErrorDifference+differenceMovementErrorSqr
        # the deviation of  movement error from the average value
        # movementVariability=math.sqrt(sumMovementErrorDifference/(len(self.frameArray)-3.0))
        # changed by Irene
        # orignally, we assume the first frame representing the start button and the last frame stands for the target.
        # so the ME of the first and end frame will be zero since these two points are lying on the task axis.
        # thus we need to exclude them when doing the division
        # But since there is 11 millisecond interval between frames,these two frames can not be exactly the start and target.
        # we do not need to exclude them now.
        movementVariability = math.sqrt(sumMovementErrorDifference / (len(self.frameArray) - 1.0)) # MV is sample standard deviation rather than standard deviation so we need to divide by length-1
        self.movementVaribility=movementVariability
        return movementVariability

    # ME
    # the average of absolute movement errors
    def calculateMovementError(self):
        sumMovementError = 0
        for i in range(0, len(self.frameArray)):
            currentFrame = self.frameArray[i]
            currentX = float(currentFrame[colNumSplitX])
            currentY = float(currentFrame[colNumSplitY])
            currentZ = float(currentFrame[colNumSplitZ])
            sumMovementError = sumMovementError + abs(self.calculateRealMovementError(self.startX, self.startY, self.startZ, self.targetX, self.targetY,
                                                                              self.targetZ, currentX, currentY, currentZ))
        # self.movementError=sumMovementError / (len(self.frameArray)-2.0)
        # changed by Irene
        # orignally, we assume the first frame representing the start button and the last frame stands for the target.
        # so the ME of the first and end frame will be zero since these two points are lying on the task axis.
        # thus we need to exclude them when doing the division
        # But since there is 11 millisecond interval between frames,these two frames can not be exactly the start and target.
        # we do not need to exclude them now.
        self.movementError = sumMovementError / len(self.frameArray)
        return self.movementError


    # the movement error of the finger location
    # this function calculates the distance between a point with the vertical plane
    # (x1,y1,z1) and (x2,y2,z2) are two points on the tablet
    # (x,y,z) is the current point
    def calculateRealMovementError(self, x1, y1, z1, x2, y2, z2, x, y, z):

        # calculate the distance between the finger point and the vertical plane
        distancePoint = getDistanceBetweenPointAndPlane(x, y, z, startThreeCor.x, startThreeCor.y, startThreeCor.z,normalVectorX, normalVectorY, normalVectorZ)

        if self.judgeAboveOrBelowPlane(x, y, z) == False:  # negative
            distancePoint = distancePoint * (-1)
        return distancePoint




    # MO is the mean movement error
    # the sum of real values with sign divided by numberOfFrame

    def calculateMovementOffset(self):

        sumMovementError = 0
        for i in range(0, len(self.frameArray)):
            currentFrame = self.frameArray[i]
            currentX = float(currentFrame[colNumSplitX])
            currentY = float(currentFrame[colNumSplitY])
            currentZ = float(currentFrame[colNumSplitZ])
            sumMovementError = sumMovementError + self.calculateRealMovementError(self.startX, self.startY, self.startZ,self.targetX, self.targetY,self.targetZ, currentX, currentY,currentZ)


        # self.movementOffset=sumMovementError/(len(self.frameArray)-2.0)
        # changed by Irene
        # orignally, we assume the first frame representing the start button and the last frame stands for the target.
        # so the ME of the first and end frame will be zero since these two points are lying on the task axis.
        # thus we need to exclude them when doing the division
        # But since there is 11 millisecond interval between frames,these two frames can not be exactly the start and target.
        # we do not need to exclude them now.
        self.movementOffset=sumMovementError/len(self.frameArray)
        return self.movementOffset




    # task axis crossing happens when the path of the finger passes through the the task plane
    # the task plane means a plane vertical to the tablet plane
    # the task plane and the tablet plane intersects at the task axis
    # this function calculate the mean frequency of task axis crossing happened per trial
    def calculateTaskAxisCrossing(self):

        startFrame=self.frameArray[0]

        # judge the initial direction
        if self.judgeAboveOrBelowPlane(float(startFrame[colNumSplitX]),float(startFrame[colNumSplitY]),float(startFrame[colNumSplitZ]))==True:
            preAbove=True
        else:
            preAbove=False

        # started from the second frame
        for  i in range(1,len(self.frameArray)):
            curFrame=self.frameArray[i]
            # judge in the current frame,
            curAbove=self.judgeAboveOrBelowPlane(float(curFrame[colNumSplitX]),float(curFrame[colNumSplitY]),float(curFrame[colNumSplitZ]))
            if curAbove!=preAbove:
                self.taskAxisCrossing=self.taskAxisCrossing+1 # task axis crossing happens
                preAbove=curAbove






    # judge whether the current point is above or below the task plane
    def judgeAboveOrBelowPlane(self,curx,cury,curz):
        # let task axis represents the line started from start point and ended with the target point
        # we can calculate the direction vector of task axis:(a,b,c)
        a=self.targetX-self.startX
        b=self.targetY-self.startY
        c=self.targetZ-self.startZ
        # let task plane represents the plane vertical to the tablet and intersect with the ipad on task axis
        # calculate the normal vector of task plane
        # it should be vertical to task axis
        # it should also be vertical to the normal vector of the tablet plane
        # the normal vector of the tablet plane is (0,1,1)
        # let (an,bn,cn) be the normal vector of task plane
        # (0,1,1)*(an,bn,cn)=0 (1)
        # (a,b,c)*(an,bn,cn)=0 (2)
        # solve the simultaneous equations of (1) and (2), we can get the (an,bn,cn)
        an=b-c
        bn=-a
        cn=a

        # since the start point is on the task plane,
        # the task plane function is an*(x-startX)+bn*(y-startY)+cn*(z-startZ)=0

        # to judge whether the point is up or below the task plane
        # put the cur point into the function
        # let an*(curX-startX)+bn*(curY-startY)+cn*(curZ-startZ)=d
        # if d > 0 , the current point is above the task plane
        # else , it is below the task plane

        calculatedValue=an*(curx-self.startX)+bn*(cury-self.startY)+cn*(curz-self.startZ)
        if calculatedValue > 0:
            return True # above the plane
        else:
            return False # below the plane


'''
# test the measures from MacKenzies
def test():
    pid=893
    block=1
    trial=3
    readFile="PID_"+str(pid)+"_Block_"+str(block)+"_Trial_"+str(trial)+".csv"
    leap=LeapAnalyzerMackenzie(readFile)
    leap.loadLeapData()
    print 'numberOfFrame', leap.calculateNumberOfFrame()
    leap.calculateMovementDirectionChange()
    print 'movementDirectionChangeX',leap.movementDirectionChangeX
    print 'movementDirectionChangeY',leap.movementDirectionChangeY
    print 'movementDirectionChangeZ',leap.movementDirectionChangeZ
    print 'MO', leap.calculateMovementOffset()
    print 'MV',leap.calculateMovementVariability(leap.movementOffset)
    print 'ME',leap.calculateMovementError()

'''


#test()





