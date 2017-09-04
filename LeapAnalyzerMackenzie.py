# seven measures from Mackenzie's paper
import csv
import math
from SpaceUtils import getDistanceOfPointAndLine
from GlobalVariables import offsetSplitX
from GlobalVariables import  offsetSplitY
from GlobalVariables import offsetSplitZ
from GlobalVariables import  path2
from GlobalVariables import  startThreeCor
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

    def __init__(self,readFile,pid,block,trial):
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

    def loadLeapData(self):
        self.frameArray=[]
        file = self.readFile
        with open(file) as f:
            f_csv = csv.reader(f)
            next(f_csv)
            for row in f_csv:
                self.frameArray.append(row)
        targetThreeCor = getTargetLocationFor3D(self.pid, self.block,
                                                self.trial)  # with accurate start coordinate in 3D,calculate the target 3D
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
        prevFrame = self.frameArray[0]
        currentFrame = self.frameArray[1]
        i = 2
        prevDirectionX = "Right"
        prevDirectionY = "Up"
        prevDirectionZ = "Forward"
        currentDirectionX = ""
        currentDirectionY = ""
        currentDirectionZ = ""
        while i < len(self.frameArray):
            prevX = float(prevFrame[offsetSplitX])
            prevY = float(prevFrame[offsetSplitY])
            prevZ = float(prevFrame[offsetSplitZ])
            currentX = float(currentFrame[offsetSplitX])
            currentY = float(currentFrame[offsetSplitY])
            currentZ = float(currentFrame[offsetSplitZ])
            currentDirectionX = self.calculateMovementDirectionChangeX(prevX, currentX, prevDirectionX, currentDirectionX) # update the self.movementDirectionChangX and return the current direction
            currentDirectionY = self.calculateMovementDirectionChangeY(prevY, currentY, prevDirectionY, currentDirectionY)
            currentDirectionZ = self.calculateMovementDirectionChangeZ(prevZ, currentZ, prevDirectionZ, currentDirectionZ)
            prevFrame = currentFrame
            currentFrame = self.frameArray[i]
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

    def calculateMovementVariability(self,movementOffset):
        sumMovementErrorDifference=0
        for i in range(0,len(self.frameArray)):
            currentFrame=self.frameArray[i]
            currentX=float(currentFrame[offsetSplitX])
            currentY=float(currentFrame[offsetSplitY])
            currentZ=float(currentFrame[offsetSplitZ])
            differenceMovementErrorSqr=math.pow(self.calculateRealMovementError(self.startX,self.startY,self.startZ,self.targetX,self.targetY,self.targetZ,currentX,currentY,currentZ)-movementOffset,2)
            sumMovementErrorDifference=sumMovementErrorDifference+differenceMovementErrorSqr
        movementVariability=math.sqrt(sumMovementErrorDifference/(len(self.frameArray)-3.0))
        self.movementVaribility=movementVariability
        return movementVariability

    # ME
    # the sum of absolute value divided by numberOfFrame
    def calculateMovementError(self):
        sumMovementError = 0
        for i in range(0, len(self.frameArray)):
            currentFrame = self.frameArray[i]
            currentX = float(currentFrame[offsetSplitX])
            currentY = float(currentFrame[offsetSplitY])
            currentZ = float(currentFrame[offsetSplitZ])
            sumMovementError = sumMovementError + abs(self.calculateRealMovementError(self.startX, self.startY, self.startZ, self.targetX, self.targetY,
                                                                              self.targetZ, currentX, currentY, currentZ))
        self.movementError=sumMovementError / (len(self.frameArray)-2.0)
        return self.movementError

    # the mean movement error
    # the sum of real values with sign divided by numberOfFrame
    def calculateMeanMovementError(self):
        sumMovementError = 0
        for i in range(0, len(self.frameArray)):
            currentFrame = self.frameArray[i]
            currentX = float(currentFrame[offsetSplitX])
            currentY = float(currentFrame[offsetSplitY])
            currentZ = float(currentFrame[offsetSplitZ])
            sumMovementError = sumMovementError + self.calculateRealMovementError(self.startX, self.startY, self.startZ, self.targetX, self.targetY,
                                                self.targetZ, currentX, currentY, currentZ)
        self.meanmovementError = sumMovementError / (len(self.frameArray) - 2.0)
        return self.meanmovementError

    # the distance of a point to the plane
    # the real value with sign
    def calculateRealMovementError(self,x1,y1,z1,x2,y2,z2,x,y,z):
        # calculate the distance between a point and a line
        distancePoint=getDistanceOfPointAndLine(x1,y1,z1,x2,y2,z2,x,y,z)
        if self.judgeUpOrBelowPlane(x,y,z)==False:
            distancePoint=distancePoint*(-1)
        #print "dis",distancePoint
        return distancePoint

    # task axis crossing happens when the path of the finger passes through the the task plane
    # the task plane means a plane vertical to the tablet plane
    # the task plane and the tablet plane intersects at the task axis
    # this function calculate the mean time of task axis crossing happened per trial
    def calculateTaskAxisCrossing(self):

        startFrame=self.frameArray[0]

        # judge the initial direction
        if self.judgeUpOrBelowPlane(float(startFrame[offsetSplitX]),float(startFrame[offsetSplitY]),float(startFrame[offsetSplitZ]))==True:
            preAbove=True
        else:
            preAbove=False

        for  i in range(1,len(self.frameArray)):
            curFrame=self.frameArray[i]
            curAbove=self.judgeUpOrBelowPlane(float(curFrame[offsetSplitX]),float(curFrame[offsetSplitY]),float(curFrame[offsetSplitZ]))
            if curAbove!=preAbove:
                self.taskAxisCrossing=self.taskAxisCrossing+1 # task axis crossing happens
                preAbove=curAbove






    # judge whether the current point is up or below the ipad plane
    def judgeUpOrBelowPlane(self,curx,cury,curz):
        # since the angle of the ipad is 45 degree,the normal vector of the ipad plane is (0,1,1)
        # we can calculate it with three points on the plane
        # let l represents the line started from start point and ended with the target point
        # we can calculate the direction vector of l
        a=self.targetX-self.startX
        b=self.targetY-self.startY
        c=self.targetZ-self.startZ
        # let n represents the plane vertical to the ipad and intersect with the ipad on l
        # calculate the normal vector of n
        # it should be vertical to l
        # it should also be vertical to the normal vector of the ipad plane
        # we calculate (an,bn,cn) the normal vector of n
        an=b-c
        bn=-a
        cn=a
        # the start point is on the plane
        # the plane function is a*(x-startX)+b*(y-startY)+c*(z-startZ)=0
        # to judge whether the point is up or below the plane
        # put the cur point into the function
        # if a*(curX-startX)+b*(curY-startY)+c*(curZ-startZ)=d
        # if d > 0 , the current point is up the plane
        # else , it is below the plane
        translateValue=an*(curx-self.startX)+bn*(cury-self.startY)+cn*(curz-self.startZ)
        if translateValue > 0:
            return True
        else:
            return False

    # MO is the mean movement error
    # the sum of real values with sign divided by numberOfFrame
    def calculateMovementOffset(self):
        sumMovementError = 0
        for i in range(0, len(self.frameArray)):
            currentFrame = self.frameArray[i]
            currentX = float(currentFrame[offsetSplitX])
            currentY = float(currentFrame[offsetSplitY])
            currentZ = float(currentFrame[offsetSplitZ])
            sumMovementError = sumMovementError + self.calculateRealMovementError(self.startX, self.startY, self.startZ, self.targetX, self.targetY,
                                                                                  self.targetZ, currentX, currentY, currentZ)
        self.movementOffset = sumMovementError / (len(self.frameArray) - 2.0)
        return self.movementOffset

# test the measures from MacKenzies
def test():
    pid=893
    block=1
    trial=3
    readFile=path2+"PID_"+str(pid)+"_Block_"+str(block)+"_Trial_"+str(trial)+".csv"
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




#test()





