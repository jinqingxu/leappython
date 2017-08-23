# seven measures from Mackenzie's paper
import csv
import math
import os
from CalculateOfCircle import get_min_max_mean_deviation_from_list
from CalculateOfCircle import calculate_3D_Dis_Of_Two_Points
from SpaceUtils import getDistanceOfPointAndLine
path = "/Users/irene/Documents/McGillUni/ACT_Research_Lab/Experiments/Motion Tracking Study/Experiment Data/split/"
class LeapAnalyzerMackenzie:
    readFile=""
    frameArray=[]
    numberFrame=0
    movementDirectionChangeX=0
    movementDirectionChangeY=0
    movementDirectionChangeZ=0
    movementOffset=0
    movementError=0
    def __init__(self,readFile):
        self.readFile=readFile

    # index of the data from split files
    offsetX=9
    offsetY=10
    offsetZ=11
    offsetTimestamp=8
    offsetSpeedX=21
    offsetSpeedY=22
    offsetSpeedZ=23
    offsetWidth=4

    def loadLeapData(self):
        file = self.readFile
        with open(file) as f:
            f_csv = csv.reader(f)
            next(f_csv)
            for row in f_csv:
                self.frameArray.append(row)

    def calculateNumberOfFrame(self):
        self.numberFrame=len(self.frameArray)
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
            prevX = float(prevFrame[self.offsetX])
            prevY = float(prevFrame[self.offsetY])
            prevZ = float(prevFrame[self.offsetZ])
            currentX = float(currentFrame[self.offsetX])
            currentY = float(currentFrame[self.offsetY])
            currentZ = float(currentFrame[self.offsetZ])
            currentDirectionX = self.calculateMovementDirectionChangeX(prevX, currentX, prevDirectionX, currentDirectionX)
            currentDirectionY = self.calculateMovementDirectionChangeY(prevY, currentY, prevDirectionY, currentDirectionY)
            currentDirectionZ = self.calculateMovementDirectionChangeZ(prevZ, currentZ, prevDirectionZ, currentDirectionZ)
            prevFrame = currentFrame
            currentFrame = self.frameArray[i]
            prevDirectionX = currentDirectionX
            prevDirectionY = currentDirectionY
            prevDirectionZ = currentDirectionZ
            i = i + 1

    def calculateMovementDirectionChangeX(self,prevX, currentX, prevDirectionX, currentDirectionX):
        if prevX != currentX:
            if currentX < prevX:
                currentDirectionX = "Right"
            else:
                currentDirectionX = "Left"
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
        differenceMovementErrorSqr=0
        firstFrame=self.frameArray[0]
        lastFrame=self.frameArray[len(self.frameArray)-1]
        startX=float(firstFrame[self.offsetX])
        startY=float(firstFrame[self.offsetY])
        startZ=float(firstFrame[self.offsetZ])
        endX=float(lastFrame[self.offsetX])
        endY=float(lastFrame[self.offsetY])
        endZ=float(lastFrame[self.offsetZ])
        for i in range(0,len(self.frameArray)):
            currentFrame=self.frameArray[i]
            currentX=float(currentFrame[self.offsetX])
            currentY=float(currentFrame[self.offsetY])
            currentZ=float(currentFrame[self.offsetZ])
            differenceMovementErrorSqr=math.pow(self.calculateRealMovementError(startX,startY,startZ,endX,endY,endZ,currentX,currentY,currentZ)-movementOffset,2)
            sumMovementErrorDifference=sumMovementErrorDifference+differenceMovementErrorSqr
        movementVariability=math.sqrt(sumMovementErrorDifference/(len(self.frameArray)-3.0))
        return movementVariability

    # ME
    # the sum of absolute value divided by numberOfFrame
    def calculateMovementError(self):
        sumMovementError = 0
        firstFrame = self.frameArray[0]
        lastFrame = self.frameArray[len(self.frameArray) - 1]
        startX = float(firstFrame[self.offsetX])
        startY = float(firstFrame[self.offsetY])
        startZ = float(firstFrame[self.offsetZ])
        endX = float(lastFrame[self.offsetX])
        endY = float(lastFrame[self.offsetY])
        endZ = float(lastFrame[self.offsetZ])
        for i in range(0, len(self.frameArray)):
            currentFrame = self.frameArray[i]
            currentX = float(currentFrame[self.offsetX])
            currentY = float(currentFrame[self.offsetY])
            currentZ = float(currentFrame[self.offsetZ])
            sumMovementError = sumMovementError + abs(self.calculateRealMovementError(startX, startY, startZ, endX, endY,
                                                                              endZ, currentX, currentY, currentZ))
        self.movementError=sumMovementError / (len(self.frameArray)-2.0)
        return self.movementError

    # the mean movement error
    # the sum of real values with sign divided by numberOfFrame
    def calculateMeanMovementError(self):
        sumMovementError = 0
        firstFrame = self.frameArray[0]
        lastFrame = self.frameArray[len(self.frameArray) - 1]
        startX = float(firstFrame[self.offsetX])
        startY = float(firstFrame[self.offsetY])
        startZ = float(firstFrame[self.offsetZ])
        endX = float(lastFrame[self.offsetX])
        endY = float(lastFrame[self.offsetY])
        endZ = float(lastFrame[self.offsetZ])
        for i in range(0, len(self.frameArray)):
            currentFrame = self.frameArray[i]
            currentX = float(currentFrame[self.offsetX])
            currentY = float(currentFrame[self.offsetY])
            currentZ = float(currentFrame[self.offsetZ])
            sumMovementError = sumMovementError + self.calculateRealMovementError(startX, startY, startZ, endX, endY,
                                                endZ, currentX, currentY, currentZ)
        self.meanmovementError = sumMovementError / (len(self.frameArray) - 2.0)
        return self.meanmovementError

    # the distance of a point to the plane
    # the real value with sign
    def calculateRealMovementError(self,x1,y1,z1,x2,y2,z2,x,y,z):
        distancePoint=getDistanceOfPointAndLine(x1,y1,z1,x2,y2,z2,x,y,z)
        if self.judgeUpOrBelowPlane(x,y,z)==False:
            distancePoint=distancePoint*(-1)
        #print "dis",distancePoint
        return distancePoint



    # judge whether the current point is up or below the ipad plane
    def judgeUpOrBelowPlane(self,curx,cury,curz):
        # since the angle of the ipad is 45 degree,the normal vector of the ipad plane is (0,1,1)
        # we can calculate it with three points on the plane
        startFrame=self.frameArray[0]
        startX=float(startFrame[self.offsetX])
        startY=float(startFrame[self.offsetY])
        startZ=float(startFrame[self.offsetZ])
        endFrame=self.frameArray[self.numberFrame-1]
        endX=float(endFrame[self.offsetX])
        endY=float(endFrame[self.offsetY])
        endZ=float(endFrame[self.offsetZ])
        # let l represents the line started from start point and ended with the target point
        # we can calculate the direction vector of l
        a=endX-startX
        b=endY-startY
        c=endZ-startZ
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
        translateValue=an*(curx-startX)+bn*(cury-startY)+cn*(curz-startZ)
        if translateValue > 0:
            return True
        else:
            return False


    def judgePause(self,speedX,speedY,speedZ):
        pauseMargin=2 # due to the measure mistake of leap motion,the pauseMargin should not be 0
        if abs(speedX)<=pauseMargin and abs(speedY)<=pauseMargin and abs(speedZ)<=pauseMargin:
            return True
        else:
            return False

    # for one trial,get the average pause duration
    def get_mean_pause_duration(self):
        minp, maxp, averagep, deviationp = get_min_max_mean_deviation_from_list(self.pauseDuration)
        return averagep

    #calculate the pause time and each pause duration
    def calculatePauseTime(self):
        i=0
        while i <self.numberFrame:
            curFrame=self.frameArray[i]
            curspeedX=float(curFrame[self.offsetSpeedX])
            curspeedY=float(curFrame[self.offsetSpeedY])
            curspeedZ=float(curFrame[self.offsetSpeedZ])
            startTime=float(curFrame[self.offsetTimestamp]) # the start time of the pause
            if self.judgePause(curspeedX,curspeedY,curspeedZ)==True:
                self.pauseTime=self.pauseTime+1
                if i==self.numberFrame-1: # if the current frame is the end one
                    self.pauseDuration.append(0) # pause time is zero
                else:
                    for j in range(i + 1, self.numberFrame):
                        nextFrame = self.frameArray[j]
                        nextspeedX = float(nextFrame[self.offsetSpeedX])
                        nextspeedY = float(nextFrame[self.offsetSpeedY])
                        nextspeedZ = float(nextFrame[self.offsetSpeedZ])
                        if self.judgePause(nextspeedX, nextspeedY, nextspeedZ) == False:
                            endTime = float(nextFrame[self.offsetTimestamp])
                            duration = endTime - startTime
                            self.pauseDuration.append(duration)
                            i=j
                            break
            i=i+1



    # MO is the mean movement error
    # the sum of real values with sign divided by numberOfFrame
    def calculateMovementOffset(self):
        sumMovementError = 0
        firstFrame = self.frameArray[0]
        lastFrame = self.frameArray[len(self.frameArray) - 1]
        startX = float(firstFrame[self.offsetX])
        startY = float(firstFrame[self.offsetY])
        startZ = float(firstFrame[self.offsetZ])
        endX = float(lastFrame[self.offsetX])
        endY = float(lastFrame[self.offsetY])
        endZ = float(lastFrame[self.offsetZ])
        for i in range(0, len(self.frameArray)):
            currentFrame = self.frameArray[i]
            currentX = float(currentFrame[self.offsetX])
            currentY = float(currentFrame[self.offsetY])
            currentZ = float(currentFrame[self.offsetZ])
            sumMovementError = sumMovementError + self.calculateRealMovementError(startX, startY, startZ, endX, endY,
                                                                                  endZ, currentX, currentY, currentZ)
        self.movementOffset = sumMovementError / (len(self.frameArray) - 2.0)
        return self.movementOffset


# for all trials in one experiment,get the percentage of trials contaning pauses
def calculate_percentage_containing_pause(pid):
    files = os.listdir(path)
    numOfFileWithPause=0 # how many files contain pause
    numOfFiles=0 # how many files of pid in total
    # PID_xxx_Block_xxx_Trial_xxx.csv
    for file in files:  # open all the file in the '/split' directory
        if not os.path.isdir(file):  # not a directory
            # a bug : if the pid is 888,files begin with pid 8881 will be taken into account
            keys = file.split('_')
            if str(pid) in keys:  # if the file begins with PID_xxx
                numOfFiles=numOfFiles+1
                if file=='PID_885_Block_1_Trial_1.csv':
                    t=0
                leap=LeapAnalyzerMackenzie(path+file)
                leap.loadLeapData()
                leap.calculateNumberOfFrame()
                leap.calculatePauseTime()
                if leap.pauseTime>0:
                    numOfFileWithPause=numOfFileWithPause+1
    percentages=numOfFileWithPause/(numOfFiles+0.0) # avoid divide integer error
    return percentages






# test the measures from MacKenzies
def test():
    readFile=path+"PID_885_Block_2_Trial_3.csv"
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




test()





