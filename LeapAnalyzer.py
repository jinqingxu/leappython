# seven measures
import csv
import math
class LeapAnalyzer:
    path = "/Users/irene/Documents/McGillUni/ACT_Research_Lab/Experiments/Motion Tracking Study/Experiment Data/split/"
    readFile=path+'PID_888_Block_1_Trial_7.csv'
    frameArray=[]
    numberFrame=0
    movementDirectionChangeX=0
    movementDirectionChangeY=0
    movementDirectionChangeZ=0
    pauseTime=0
    pauseDuration=[]
    spiralTime=0
    spiralDuration=[]
    movementOffset=0
    movementError=0
    offsetX=9
    offsetY=10
    offsetZ=11
    offsetTimestamp=8
    offsetSpeedX=21
    offsetSpeedY=22
    offsetSpeedZ=23
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
        distanceLine=self.calculateLineDistance(x1,y1,z1,x2,y2,z2)
        pow1=math.pow((x1-x)*(y2-y1)-(y1-y)*(x2-x1),2)
        pow2=math.pow((y1-y)*(z2-z1)-(z1-z)*(y2-y1),2)
        pow3=math.pow((z1-z)*(x2-x1)-(x1-x)*(z2-z1),2)
        distancePoint=math.sqrt(pow1+pow2+pow3)/distanceLine # the area of the parallelogram divided by the length of the edge is the distance of a point to a line in 3D cors
        if self.judgeUpOrBelowPlane(x,y,z)==False:
            distancePoint=distancePoint*(-1)
        #print "dis",distancePoint
        return distancePoint

    def calculateLineDistance(self,x1,y1,z1,x2,y2,z2):
        return math.sqrt((math.pow((x1-x2),2) + math.pow((y1-y2),2) + math.pow((z1-z2),2)))


    # judge whether the current point is up or below the laptop plane
    def judgeUpOrBelowPlane(self,curx,cury,curz):
        # since the angle of the laptop is 45 degree,the normal vector of the laptop plane is (0,1,1)
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
        # let n represents the plane vertical to the laptop and intersect with the laptop on l
        # calculate the normal vector of n
        # it should be vertical to l
        # it should also be vertical to the normal vector of the laptop plane
        # we calculate (an,bn,cn) the normal vector of n
        an=b-c
        bn=-a
        cn=a
        # the start point is on the plane
        # the plane function is a*(x-startX)+b*(y-startY)+c*(z-startZ)=0
        # to judge whether the point is up or below the plane
        # put the cur point into the function
        # if a*(curX-startX)+b*(curY-startY)+c*(curZ-startZ)=d
        # that equals a*(curX-startX)+b*(curY-startY)+c*(curZ-startZ-d/c)=0
        # that means the original plane has to translate d/c to become the current plane
        # if d/c > 0 , the current point is up the plane
        # else , it is below the plane
        translateValue=(an*(curx-startX)+bn*(cury-startY)+cn*(curz-startZ))/cn
        if translateValue > 0:
            return True
        else:
            return False


    def judgePause(self,speedX,speedY,speedZ):
        pauseMargin=0.002 # due to the measure mistake of leap motion,the pauseMargin should not be 0
        if abs(speedX)<=pauseMargin and abs(speedY)<=pauseMargin and abs(speedZ)<=pauseMargin:
            return True
        else:
            return False

    #calculate the pause time and each pause duration
    def calculatePauseTime(self):
        for i in range(0,self.numberFrame):
            curFrame=self.frameArray[i]
            curspeedX=float(curFrame[self.offsetSpeedX])
            curspeedY=float(curFrame[self.offsetSpeedY])
            curspeedZ=float(curFrame[self.offsetSpeedZ])
            if curspeedY==1.2:
                t=0
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
                            break

    def judgeNearTarget(self,curX,curY,curZ,targetX,targetY,targetZ):
        margin=5 # judge the distance of near
        distance=math.sqrt(math.pow(curX-targetX,2)+math.pow(curY-targetY,2)+math.pow(curZ-targetZ,2))
        if distance<margin:
            return True
        else:
            return False

    # row[0] is the start point,it represents the start point
    # row[row.length-1] is the end point,it represents the target point
    def calculateSpiralDuration(self):
        targetFrame=self.frameArray[self.numberFrame-1] # end frame represent the target
        targetX=float(targetFrame[self.offsetX])
        targetY=float(targetFrame[self.offsetY])
        targetZ=float(targetFrame[self.offsetZ])
        for i in range(1,self.numberFrame-1): # skip the start and end frame
            curFrame=self.frameArray[i]
            curX=float(curFrame[self.offsetX])
            curY=float(curFrame[self.offsetY])
            curZ=float(curFrame[self.offsetZ])
            if self.judgeNearTarget(curX,curY,curZ,targetX,targetY,targetZ)==True:
                self.spiralTime=self.spiralTime+1
                startTime=float(curFrame[self.offsetTimestamp]) # the start time of the spiral
                if i==self.numberFrame-2: # if the current one if the one before the end one
                    nextFrame = self.frameArray[self.numberFrame-1]
                    endTime = float(nextFrame[self.offsetTimestamp])
                    duration = endTime - startTime
                    self.spiralDuration.append(duration)
                else:
                    for j in range(i + 1, self.numberFrame - 1):
                        nextFrame = self.frameArray[j]
                        nextX = float(nextFrame[self.offsetX])
                        nextY = float(nextFrame[self.offsetY])
                        nextZ = float(nextFrame[self.offsetZ])
                        if self.judgeNearTarget(nextX, nextY, nextZ, targetX, targetY,
                                                targetZ) == False or j == self.numberFrame - 2:  # stop spiral or arriving at the last frame
                            endTime = float(nextFrame[self.offsetTimestamp])
                            duration = endTime - startTime
                            self.spiralDuration.append(duration)
                            break

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

# get the min(l),max(l),avergae(l),difference of min and max
def get_min_max_mean_deviation_from_list(l):
    min_l = float(l[0])
    max_l = float(l[0])
    sum_l = 0
    for i in range(0, len(l)):
        if float(l[i]) > max_l:
            max_l = float(l[i])
        if float(l[i]) < min_l:
            min_l = float(l[i])
        sum_l += float(l[i])
    return min_l, max_l, sum_l / (len(l) + 0.0), max_l - min_l

# test the lepa analyzer functions
def test():
    leap=LeapAnalyzer()
    leap.loadLeapData()
    print 'numberOfFrame', leap.calculateNumberOfFrame()
    leap.calculateMovementDirectionChange()
    print 'movementDirectionChangeX',leap.movementDirectionChangeX
    print 'movementDirectionChangeY',leap.movementDirectionChangeY
    print 'movementDirectionChangeZ',leap.movementDirectionChangeZ
    print 'MO', leap.calculateMovementOffset()
    print 'MV',leap.calculateMovementVariability(leap.movementOffset)
    print 'ME',leap.calculateMovementError()
    leap.calculatePauseTime()
    print 'pauseTime',leap.pauseTime
    if leap.pauseTime>0:
        pDuration = leap.pauseDuration
        print 'pauseDuration:'
        minp,maxp,averagep,deviationp=get_min_max_mean_deviation_from_list(pDuration)
        print 'min:',minp,' max:',maxp,' average:',averagep,' deviation:',deviationp
    leap.calculateSpiralDuration()
    print 'spiralTime',
    print leap.spiralTime
    if leap.spiralTime>0:
        print 'spiralDuration',
        sDuration=leap.spiralDuration
        mins,maxs,averages,deviations=get_min_max_mean_deviation_from_list(sDuration)
        print 'min:',mins,' max:',maxs,' average:',averages,' deviations:',deviations




test()




