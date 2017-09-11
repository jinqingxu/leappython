# the original measurements not from the paper
import csv
from CalculateOfCircle import get_min_max_mean_deviation_from_list
from CalculateOfCircle import calculate_3D_Dis_Of_Two_Points
from SpaceUtils import  getIntersactionPointOfPointAndPlane
from GlobalVariables import path2
from GlobalVariables import offsetSplitX
from GlobalVariables import  offsetSplitY
from GlobalVariables import offsetSplitZ
from GlobalVariables import  offsetSplitTimestamp
from GlobalVariables import  offsetSplitWidth
from SpaceUtils import getTargetLocationFor3D

class LeapAnalyzerOriginal:
    pid = 0
    block = 0
    trial = 0
    readFile=""
    frameArray=[]
    numberFrame=0
    decisionMakingTime=0
    decisionMakingDuration=[]
    meanDecideMakingDuration=0
    targetX = 0
    targetY = 0
    targetZ = 0
    def __init__(self,readFile,pid,block,trial):
        self.frameArray=[]
        self.numberFrame=0
        self.readFile=readFile
        self.decisionMakingTime = 0
        self.decisionMakingDuration = []
        self.meanDecideMakingDuration = 0
        self.pid=pid
        self.block=block
        self.trial=trial

    def loadLeapData(self):
        file = self.readFile
        self.frameArray=[]
        with open(file) as f:
            f_csv = csv.reader(f)
            next(f_csv)
            for row in f_csv:
                self.frameArray.append(row)
        self.numberFrame=len(self.frameArray)
        targetThreeCor = getTargetLocationFor3D(self.pid, self.block,
                                                self.trial)  # with accurate start coordinate in 3D,calculate the target 3D
        self.targetX = targetThreeCor.x
        self.targetY = targetThreeCor.y
        self.targetZ = targetThreeCor.z

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
        # let the line vertical to the plane and  passing through curX,curY,curZ  be l
        # this function calculate the intersaction point of l and the plane
        # the normal vector of the tablet plane is (0,1,1)
        intersactionX,intersactionY,intersactionZ=getIntersactionPointOfPointAndPlane(curX,curY,curZ,targetX,targetY,targetZ,0,1,1)
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
    def calculateDecisionMakingDuration(self):
        targetFrame = self.frameArray[self.numberFrame - 1]  # end frame represent the target
        width=float(targetFrame[offsetSplitWidth])
        i=1 # skip the start frame
        while i < self.numberFrame-1: # skip the end frame
            curFrame=self.frameArray[i]
            curX=float(curFrame[offsetSplitX])
            curY=float(curFrame[offsetSplitY])
            curZ=float(curFrame[offsetSplitZ])
            if self.judgeNearTarget(curX,curY,curZ,self.targetX,self.targetY,self.targetZ,width)==True:
                self.decisionMakingTime=self.decisionMakingTime+1
                startTime=float(curFrame[offsetSplitTimestamp]) # the start time of the spiral
                if i==self.numberFrame-2: # if the current one is the one before the end one,the loop beneath will not be executed
                    nextFrame = self.frameArray[self.numberFrame-1]
                    endTime = float(nextFrame[offsetSplitTimestamp])
                    duration = endTime - startTime
                    self.decisionMakingDuration.append(duration)
                else:
                    for j in range(i + 1, self.numberFrame - 1):
                        nextFrame = self.frameArray[j]
                        nextX = float(nextFrame[offsetSplitX])
                        nextY = float(nextFrame[offsetSplitY])
                        nextZ = float(nextFrame[offsetSplitZ])
                        if self.judgeNearTarget(nextX, nextY, nextZ, self.targetX, self.targetY,
                                                self.targetZ,width) == False or j == self.numberFrame - 2:  # stop spiral or arriving at the last frame
                            endTime = float(nextFrame[offsetSplitTimestamp])
                            duration = endTime - startTime
                            self.decisionMakingDuration.append(duration)
                            i=j # find the next spiral
                            break
            i=i+1
        mind, maxd, averaged, deviationd = get_min_max_mean_deviation_from_list(self.decisionMakingDuration) # get the statistics of the decisionMaking list
        self.meanDecideMakingDuration=averaged







# test the measures from MacKenzies
def test():
    readFile=path2+"PID_901_Block_1_Trial_3.csv"
    leap=LeapAnalyzerOriginal(readFile)
    leap.loadLeapData()
    print 'numberOfFrame', leap.calculateNumberOfFrame()
    leap.calculateDecisionMakingDuration()
    print 'decisionMakingTime',
    print leap.decisionMakingTime
    if leap.decisionMakingTime>0:
        print 'decisionMakingDuration',
        sDuration=leap.decisionMakingDuration
        mins,maxs,averages,deviations=get_min_max_mean_deviation_from_list(sDuration)
        print 'min:',mins,' max:',maxs,' average:',averages,' deviations:',deviations




#test()




