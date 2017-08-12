# seven measures
import csv
import math
class LeapAnalyzer:
    path = "/Users/irene/Documents/McGillUni/ACT_Research_Lab/Experiments/Motion Tracking Study/Experiment Data/"
    readFile=path+'Pid_777_Block_0_Trial_1.csv'
    frameArray=[]
    offset=3
    numberFrame=0
    movementDirectionChangeX=0
    movementDirectionChangeY=0
    movementDirectionChangeZ=0
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
            prevX = float(prevFrame[3 + self.offset])
            prevY = float(prevFrame[4 + self.offset])
            prevZ = float(prevFrame[5 + self.offset])
            currentX = float(currentFrame[3 + self.offset])
            currentY = float(currentFrame[4 + self.offset])
            currentZ = float(currentFrame[5 + self.offset])
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

    def calculateMovementVariability(self,meanMovementError):
        sumMovementErrorDifference=0
        differenceMovementErrorSqr=0
        firstFrame=self.frameArray[0]
        lastFrame=self.frameArray[len(self.frameArray)-1]
        startX=float(firstFrame[3+self.offset])
        startY=float(firstFrame[4+self.offset])
        startZ=float(firstFrame[5+self.offset])
        endX=float(lastFrame[3+self.offset])
        endY=float(lastFrame[4+self.offset])
        endZ=float(lastFrame[5+self.offset])
        for i in range(0,len(self.frameArray)):
            currentFrame=self.frameArray[i]
            currentX=float(currentFrame[3+self.offset])
            currentY=float(currentFrame[4+self.offset])
            currentZ=float(currentFrame[5+self.offset])
            differenceMovementErrorSqr=math.pow(self.calculateMovementError(startX,startY,startZ,endX,endY,endZ,currentX,currentY,currentZ)-meanMovementError,2)
            sumMovementErrorDifference=sumMovementErrorDifference+differenceMovementErrorSqr
        movementVariability=math.sqrt(sumMovementErrorDifference/(len(self.frameArray)-3))
        return movementVariability

    def calculateMeanMovementError(self):
        sumMovementError = 0
        firstFrame = self.frameArray[0]
        lastFrame = self.frameArray[len(self.frameArray) - 1]
        startX = float(firstFrame[3 + self.offset])
        startY = float(firstFrame[4 + self.offset])
        startZ = float(firstFrame[5 + self.offset])
        endX = float(lastFrame[3 + self.offset])
        endY = float(lastFrame[4 + self.offset])
        endZ = float(lastFrame[5 + self.offset])
        for i in range(0, len(self.frameArray)):
            currentFrame = self.frameArray[i]
            currentX = float(currentFrame[3 + self.offset])
            currentY = float(currentFrame[4 + self.offset])
            currentZ = float(currentFrame[5 + self.offset])
            sumMovementError = sumMovementError + self.calculateMovementError(startX, startY, startZ, endX, endY,
                                                                              endZ, currentX, currentY, currentZ)
        meanMovementError = sumMovementError / (len(self.frameArray)-2)
        return meanMovementError

    def calculateMovementError(self,x1,y1,z1,x2,y2,z2,x,y,z):
        distanceLine=self.calculateLineDistance(x1,y1,z1,x2,y2,z2)
        pow1=math.pow((x1-x)*(y2-y1)-(y1-y)*(x2-x1),2)
        pow2=math.pow((y1-y)*(z2-z1)-(z1-z)*(y2-y1),2)
        pow3=math.pow((z1-z)*(x2-x1)-(x1-x)*(z2-z1),2)
        distancePoint=math.sqrt(pow1+pow2+pow3)/distanceLine
        return distancePoint

    def calculateLineDistance(self,x1,y1,z1,x2,y2,z2):
        return math.sqrt((math.pow((x1-x2),2) + math.pow((y1-y2),2) + math.pow((z1-z2),2)))
    #todo
    def calculateMovementOffset(self,x1,y1,z1,x2,y2,z2,x,y,z):
        return 0.0

# test the lepa analyzer functions
def test():
    leap=LeapAnalyzer()
    leap.loadLeapData()
    print leap.calculateNumberOfFrame()
    leap.calculateMovementDirectionChange()
    print leap.movementDirectionChangeX
    print leap.movementDirectionChangeY
    print leap.movementDirectionChangeZ
    meanMovementError=leap.calculateMeanMovementError()
    print leap.calculateMovementVariability(meanMovementError)

test()




