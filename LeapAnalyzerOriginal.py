# the original measurements not from the paper
import csv
import math
import os
from CalculateOfCircle import get_min_max_mean_deviation_from_list
from CalculateOfCircle import calculate_3D_Dis_Of_Two_Points
from SpaceUtils import getIntersactionPointOfLineAndPlane
path = "/Users/irene/Documents/McGillUni/ACT_Research_Lab/Experiments/Motion Tracking Study/Experiment Data/split/"
class LeapAnalyzerOriginal:
    readFile=""
    frameArray=[]
    numberFrame=0
    spiralTime=0
    spiralDuration=[]
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

    # let the finger point be p ,the ipad plane be A, the line passing though p and vertical to A be l
    # let the intersaction of l and A be c
    # spiral should meet two conditions
    # firstly, c should be inside the circle with the redius of 5/4 target redius
    # secondly,the distance between p and A should be very small
    def judgeNearTarget(self,curX,curY,curZ,targetX,targetY,targetZ,width):
        margin=15 # the max distance of p and A
        intersactionX,intersactionY,intersactionZ=getIntersactionPointOfLineAndPlane(curX,curY,curZ,targetX,targetY,targetZ)
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




    # spiral means the finger is very close to the ipad
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







# test the measures from MacKenzies
def test():
    readFile=path+"PID_885_Block_2_Trial_3.csv"
    leap=LeapAnalyzerOriginal(readFile)
    leap.loadLeapData()
    print 'numberOfFrame', leap.calculateNumberOfFrame()
    leap.calculateSpiralDuration()
    print 'spiralTime',
    print leap.spiralTime
    if leap.spiralTime>0:
        print 'spiralDuration',
        sDuration=leap.spiralDuration
        mins,maxs,averages,deviations=get_min_max_mean_deviation_from_list(sDuration)
        print 'min:',mins,' max:',maxs,' average:',averages,' deviations:',deviations




test()





