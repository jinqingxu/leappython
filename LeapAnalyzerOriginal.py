# author:Irene
# the original measurements not from the paper
# already add comments

import csv
from CalculateOfCircle import get_min_max_mean_deviation_from_list
from CalculateOfCircle import calculate_3D_Dis_Of_Two_Points
from SpaceUtils import  getIntersactionPointOfPointAndPlane


from GlobalVariables import *
from SpaceUtils import getTargetLocationFor3D


# deciding making is a measure representing uncertainty
# a supplement for verification time
# an original measure brought up by our work

class LeapAnalyzerOriginal:

    pid = 0
    block = 0
    trial = 0
    readFile=""
    frameArray=[]
    numberFrame=0
    decisionMakingTime=0 # how many times decision making happend
    decisionMakingDuration=[] # the duration list
    meanDecideMakingDuration=0 # the mean time duration of decision meaning in a trial
    targetX = 0
    targetY = 0
    targetZ = 0
    path=""
    def __init__(self,readFile,pid,block,trial,path):
        self.frameArray=[]
        self.numberFrame=0
        self.readFile=readFile
        self.decisionMakingTime = 0
        self.decisionMakingDuration = []
        self.meanDecideMakingDuration = 0
        self.pid=pid
        self.block=block
        self.trial=trial
        self.path=path

    def loadLeapData(self):
        file = self.readFile
        self.frameArray=[]
        with open(file) as f:
            f_csv = csv.reader(f)
            next(f_csv)
            for row in f_csv:
                self.frameArray.append(row)
        self.numberFrame=len(self.frameArray)
        targetThreeCor = getTargetLocationFor3D(self.pid, self.block,self.trial,self.path)  # with accurate start coordinate in 3D,calculate the target 3D
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
        # the definition of this function is in the SpaceUtil.py
        intersactionX,intersactionY,intersactionZ=getIntersactionPointOfPointAndPlane(curX,curY,curZ,targetX,targetY,targetZ,normalVectorX,normalVectorY,normalVectorZ)
        # find the distance between p and A
        dis=calculate_3D_Dis_Of_Two_Points(curX,curY,curZ,intersactionX,intersactionY,intersactionZ)
        if dis > margin:
            return False
        else: # dis should be smaller or equal to margin
            # calculate the distance between target and intersaction point c
            dis2=calculate_3D_Dis_Of_Two_Points(targetX,targetY,targetZ,intersactionX,intersactionY,intersactionZ)
            margin2=(1+1/4)*width # the max distance of A and target center
            if dis2 > margin2:
                return False
            else:
                return True




    # decision meaking means the finger is very close to the tablet and near the target
    def calculateDecisionMakingDuration(self):
        endFrame = self.frameArray[self.numberFrame - 1]  # end Frame is the last frame
        width=float(endFrame[colNumSplitWidth]) # the width of the target
        i=1 # skip the start frame
        while i < self.numberFrame-1: # skip the end frame
            curFrame=self.frameArray[i]
            curX=float(curFrame[colNumSplitX])
            curY=float(curFrame[colNumSplitY])
            curZ=float(curFrame[colNumSplitZ])
            if self.judgeNearTarget(curX,curY,curZ,self.targetX,self.targetY,self.targetZ,width)==True: # decisionMaking started
                self.decisionMakingTime=self.decisionMakingTime+1
                startTime=float(curFrame[colNumSplitTimestamp]) # the start time of the spiral
                # if the current one is the one before the end one,the loop  will not be executed since the end Frame should be frame[numberOfFrame-1]
                if i==self.numberFrame-2:
                    nextFrame = self.frameArray[self.numberFrame-1]
                    endTime = float(nextFrame[colNumSplitTimestamp])
                    duration = endTime - startTime
                    self.decisionMakingDuration.append(duration)
                else:
                    for j in range(i + 1, self.numberFrame - 1):
                        nextFrame = self.frameArray[j]
                        nextX = float(nextFrame[colNumSplitX])
                        nextY = float(nextFrame[colNumSplitY])
                        nextZ = float(nextFrame[colNumSplitZ])
                        # stop decisionMaking or arriving at the last frame
                        if self.judgeNearTarget(nextX, nextY, nextZ, self.targetX, self.targetY,self.targetZ,width) == False or j == self.numberFrame - 2:
                            endTime = float(nextFrame[colNumSplitTimestamp])
                            duration = endTime - startTime
                            self.decisionMakingDuration.append(duration)
                            i=j # find the next spiral
                            break
            i=i+1
        mind, maxd, averaged, deviationd = get_min_max_mean_deviation_from_list(self.decisionMakingDuration) # get the statistics of the decisionMaking list
        self.meanDecideMakingDuration=averaged






'''
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

'''


#test()




