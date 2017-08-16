# seven measures
import csv
import math
from CalculateOfCircle import get_min_max_mean_deviation_from_list
from CalculateOfCircle import calculate_3D_Dis_Of_Two_Points
class LeapAnalyzer:
    path = "/Users/irene/Documents/McGillUni/ACT_Research_Lab/Experiments/Motion Tracking Study/Experiment Data/split/"
    readFile=path+'PID_884_Block_1_Trial_3.csv'
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
        pauseMargin=2 # due to the measure mistake of leap motion,the pauseMargin should not be 0
        if abs(speedX)<=pauseMargin and abs(speedY)<=pauseMargin and abs(speedZ)<=pauseMargin:
            return True
        else:
            return False

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


    # let the finger point be p ,the laptop plane be A, the line passing though p and vertical to A be l
    # let the intersaction of l and A be c
    # spiral should meet two conditions
    # firstly, c should be inside the circle with the redius of 5/4 target redius
    # secondly,the distance between p and A should be very small
    def judgeNearTarget(self,curX,curY,curZ,targetX,targetY,targetZ,width):
        margin=15 # the max distance of p and A
        # since the angle of the laptop is 45 degree,the normal vector of the laptop plane is (0,1,1)
        # so the function of line l is (x-curX)/0=(y-curY)/1=(z-curZ)/1 ,that is y-curY=z-curZ=k
        # let y=curY+k,z=curZ+k
        # the function of the laptop is 0*(x-targetX)+1*(y-targetY)+1*(z-targetZ)=0
        # put y and z into the laptop function
        # k=(targetY+targetZ-curY-curZ)/2
        # so y=curY+k=(targetY+targetZ+curY-curZ)/2
        # z=curZ+k=(targetY+targetZ+curZ-curY)/2
        # x=curX
        intersactionX=curX
        intersactionY=(targetY+targetZ+curY-curZ)/2
        intersactionZ=(targetY+targetZ+curZ-curY)/2
        # find the distance between p and A
        dis=calculate_3D_Dis_Of_Two_Points(curX,curY,curZ,intersactionX,intersactionY,intersactionZ)
        if dis > margin:
            return False
        else: # dis should be smaller or equal to margin
            dis2=calculate_3D_Dis_Of_Two_Points(targetX,targetY,targetZ,intersactionX,intersactionY,intersactionZ)
            margin2=(1+1/4)*width # the max distance of A and target center
            if dis2 > margin2:
                return False
            else:
                return True




    # spiral means the finger is very close to the laptop
    # and is within the 5/4 redius circle
    def calculateSpiralDuration(self):
        targetFrame=self.frameArray[self.numberFrame-1] # end frame represent the target
        targetX=float(targetFrame[self.offsetX])
        targetY=float(targetFrame[self.offsetY])
        targetZ=float(targetFrame[self.offsetZ])
        width=float(targetFrame[self.offsetWidth])
        i=1 # skip the start frame
        while i < self.numberFrame-1: # skip the end frame
            curFrame=self.frameArray[i]
            curX=float(curFrame[self.offsetX])
            curY=float(curFrame[self.offsetY])
            curZ=float(curFrame[self.offsetZ])
            if self.judgeNearTarget(curX,curY,curZ,targetX,targetY,targetZ,width)==True:
                self.spiralTime=self.spiralTime+1
                startTime=float(curFrame[self.offsetTimestamp]) # the start time of the spiral
                if i==self.numberFrame-2: # if the current one is the one before the end one,the loop beneath will not be executed
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
                                                targetZ,width) == False or j == self.numberFrame - 2:  # stop spiral or arriving at the last frame
                            endTime = float(nextFrame[self.offsetTimestamp])
                            duration = endTime - startTime
                            self.spiralDuration.append(duration)
                            i=j # find the next spiral
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




