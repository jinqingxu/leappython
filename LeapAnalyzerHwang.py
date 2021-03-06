# the measures from huang's paper

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import csv
import math
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# import helper functions from other script
from CalculateOfCircle import get_min_max_mean_deviation_from_list
from SpaceUtils import calculate_3D_Dis_Of_Two_Points
from GlobalVariables import *


from FileUtils import getSortedSplitFile
from SpaceUtils import getTargetLocationFor3D
from SpaceUtils import getDistanceBetweenPointAndPlane

class SubMovement:

    startTime=0 # the start time of frame
    endTime=0 # the end time of frame
    startX=0
    startY=0
    startZ=0
    endX=0
    endY=0
    endZ=0
    peekSpeed = 0.0
    duration = 0.0  # how long does the submovement last ,the unit is in mm

    '''
    coincidentErrorValue=0
    coincidentErrorType=""
    perpendicularError=0
    '''

    def __init__(self,startTime,endTime,startX,startY,startZ,endX,endY,endZ,peekSpeed,duration):

        self.startTime=startTime # the start timestamp of a submovement
        self.endTime=endTime
        self.startX=startX # the start location of a submovement
        self.startY=startY
        self.startZ=startZ
        self.endX=endX
        self.endY=endY
        self.endZ=endZ
        self.peekSpeed=peekSpeed
        self.duration=duration

        '''
        self.coincidentErrorValue=coincidentErrorValue
        self.coincidentErrorType=coincidentErrorType
        '''


class LeapAnalyzerHwang:

    # LeapAnalyzerHuang is focus on a specific trial
    pid=0
    block=0
    trial=0
    readFile="" # the trial file
    frameArray=[]
    numberFrame=0

    # variables for the peek submovement speed
    tmpPeekSpeed=0 # temporary variable for submovement peek speed
    trialPeekSpeed=0 # peek submovement speed in the whole trial

    # variables for the pasue
    meanPauseDuration=0 # the average pause duration in one trial
    pauseFrequency=0  # how many times pauses happen
    pauseDuration=[] # the duration of pause
    pauseLocation=[] # the distribution of pause location
    pauseMarginSpeed=0.01 # due to the measure mistake of leap motion,the pauseMargin should not be 0

    # variables for judging the start and end of a submovement
    brakeMarginAcc=1 # if the acc is up to brakeMarginAcc,that means the end of the submovement
    submovement_list=[] # the list of submovements

    width=0 # the width of the target

    # the location of the target,initialized in the loaddata function
    targetX=0
    targetY=0
    targetZ=0

    finalLiftUpTime=0  # the timestamp of the final lift up

    verificationTime=0.0 # the verification time,the duration from the end of the last submovement to the end of the trial

    path=""

    # initialize
    def __init__(self,readFile,pid,block,trial,path):

        self.readFile=readFile
        self.pid=pid
        self.block=block
        self.trial=trial
        self.submovement_list=[]
        self.frameArray = []
        self.numberFrame = 0
        self.tmpPeekSpeed = 0  # temporary variable for submovement peek speed
        self.trialPeekSpeed = 0  # peek speed in the whole trial
        self.meanPauseDuration = 0
        self.pauseTime = 0
        self.pauseDuration = []
        self.pauseLocation = []
        self.verificationTime=0.0
        self.path=path


    def loadLeapData(self):

        file = self.readFile # the trial data file
        self.frameArray=[]

        with open(file) as f:
            f_csv = csv.reader(f)
            next(f_csv) # skip the header
            for row in f_csv:
                self.frameArray.append(row) # fullfil the frameArray

        self.numberFrame = len(self.frameArray)
        firstFrame=self.frameArray[0] # the first frame of a trial
        self.width=float(firstFrame[colNumSplitWidth]) # the width of target
        finalLiftUpFrame=self.frameArray[self.numberFrame-1] # the final lift up frame of a trial

        targetThreeCor=getTargetLocationFor3D(self.pid,self.block,self.trial,self.path) # with accurate start coordinate in 3D,calculate the target 3D

        self.targetX=targetThreeCor.x
        self.targetY=targetThreeCor.y
        self.targetZ=targetThreeCor.z

        self.finalLiftUpTime=float(finalLiftUpFrame[colNumSplitTimestamp])



    def calculateNumberOfFrame(self): # the length of self.frameArray
        return self.numberFrame

    '''
    # this function is not used any more
    # this function is help to decide whether the submovement is slipOff or before final selection
    # let the finger point be p ,the laptop plane be A, the line passing though p and vertical to A be l
    # let the intersaction of l and A be c
    # spiral should meet two conditions
    # firstly, c should be inside the target
    # secondly,the distance between p and A should be very small
    def judgeInsideTarget(self, curX, curY, curZ, targetX, targetY, targetZ, width):
        margin = 15  # the max distance of p and A
        intersactionX, intersactionY, intersactionZ=getDistanceBetweenPointAndPlane(curX,curY,curZ,targetX,targetY,targetZ,normalVectorX,normalVectorY,normalVectorZ)
        # find the distance between p and A
        dis = calculate_3D_Dis_Of_Two_Points(curX, curY, curZ, intersactionX, intersactionY, intersactionZ)
        if dis > margin: # dis should be smaller or equal to margin
            return False
        else:
            # dis2 means the distance between the intersaction point and the center of the target
            dis2 = calculate_3D_Dis_Of_Two_Points(targetX, targetY, targetZ, intersactionX, intersactionY,
                                                  intersactionZ)
            if dis2 > width: # dis2 must be smaller than the radius of the circle which means the intersaction point should be located inside the target
                return False
            else:
                return True
    '''

    # the current speed is near zero
    def judgePause(self,speed):
        if speed < self.pauseMarginSpeed: # pauseMarginSpeed is the maximum of pause speed which is 0.01
            return True
        else:
            return False

    # for one trial,get the average pause duration
    # the unit of duration is ms
    def getMeanPauseDuration(self):
        if len(self.pauseDuration)==0: # if the pause duration list is empty,return 0
            return 0
        minp, maxp, averagep, deviationp = get_min_max_mean_deviation_from_list(self.pauseDuration) # get the statistic value of the puase duration list
        self.meanPauseDuration=averagep # the average pause duration
        return averagep

    # record the pause location
    # append it in the pauseLoction
    # the location means the distance between the current location and the target
    def calculatePauseLocation(self,curX,curY,curZ):

        dis=calculate_3D_Dis_Of_Two_Points(curX,curY,curZ,self.targetX,self.targetY,self.targetZ)
        self.pauseLocation.append(dis)

    #calculate the pause time and each pause duration
    # no return value
    # change the value of self.pauseTime,self.pauseDuration
    def calculatePause(self):
        i=0
        while i <self.numberFrame:
            curFrame=self.frameArray[i] # the current frame
            curSpeed=float(curFrame[colNumSplitSpeed]) # the speed of the current frame
            startTime=float(curFrame[colNumSplitTimestamp]) # the start time of the pause

            # find the start frame of pause
            if self.judgePause(curSpeed) == True: #  pause meansthe speed is within the pauseMargin

                self.pauseFrequency=self.pauseFrequency+1 # pauseTime means how many times do pauses happen
                curX=float(curFrame[colNumSplitX]) # currate X location
                curY=float(curFrame[colNumSplitY])
                curZ=float(curFrame[colNumSplitZ])
                self.calculatePauseLocation(curX,curY,curZ) # the location means the distance between the current location and the target
                if i==self.numberFrame-1: # if the current frame is the end one

                    self.pauseDuration.append(0) # pause time is zero
                else:

                    for j in range(i + 1, self.numberFrame): # find the end frame of the pause

                        nextFrame = self.frameArray[j]
                        nextSpeed=float(nextFrame[colNumSplitSpeed]) # nextSpeed means the speed of next frame
                        if self.judgePause(nextSpeed) == False: # if the nextSpeed is not within the pause Margin,that means the end of the pause
                            endTime = float(nextFrame[colNumSplitTimestamp]) # the end time of a pause
                            duration = endTime - startTime  # the duration of a pause
                            self.pauseDuration.append(duration) # save the duration in a duration list for a trial
                            i=j # to find the start of next pause,loop started from frameArray[j+1]
                            break
            i=i+1

        self.getMeanPauseDuration() # calculate the mean value of pause durations and set the value of self.meanPauseDuration

    '''
    # this function will not be used anymore
    # get number of submovements before final entry
    # be inside the target but before lift up
    # alsp get number of submovements slip off
    # return numBeforeFinal,numSlipOff
    def getNumOfSubmovementInTwoSets(self):

        numBeforeFinal=0 # number of submovements before final lift up
        numSlipOff=0 # number of submovements slip off

        for s in self.submovement_list:
            if self.judgeInsideTarget(s.startX,s.startY,s.startZ,self.targetX,self.targetY,self.targetZ,self.width)==True: # the start of the submovement is inside the target

                if self.judgeInsideTarget(s.endX,s.endY,s.endZ,self.targetX,self.targetY,self.targetZ,self.width)==True: # before the final entry
                    numBeforeFinal=numBeforeFinal+1
                else: # the start is inside the target,the end is outside the target.That means slip off
                    numSlipOff=numSlipOff+1

        return numBeforeFinal,numSlipOff
    '''

    # go through the self.Frames
    # find all submovements and put them into submovement_list
    def getSubmovements(self):

        index = 0 # the current index of frame

        while index < self.numberFrame:

            index = self.getSubmovementStart(index)  # the start index of the submovement
            startIndex = index
            startTime = float(self.frameArray[startIndex][colNumSplitTimestamp])
            startX = float(self.frameArray[startIndex][colNumSplitX])
            startY = float(self.frameArray[startIndex][colNumSplitY])
            startZ = float(self.frameArray[startIndex][colNumSplitZ])
            if startIndex == -1:  # there is no submovements int the future
                break

            index = self.getSubmovementEnd(startIndex + 1)  # the end Index must be after the startIndex, so start at startIndex+1
            endIndex = index
            endX = float(self.frameArray[endIndex][colNumSplitX])
            endY = float(self.frameArray[endIndex][colNumSplitY])
            endZ = float(self.frameArray[endIndex][colNumSplitZ])
            endTime = float(self.frameArray[endIndex][colNumSplitTimestamp])

            # relaendX,relaendY,relaendZ=self.getRelativeCors(endX,endY,endZ)
            # coincidentErrorValue,coincidentErrorType=self.calculateCoincidentError(endX)

            if self.tmpPeekSpeed > self.trialPeekSpeed:
                self.trialPeekSpeed = self.tmpPeekSpeed

            self.submovement_list.append(
                SubMovement(startTime, endTime, startX, startY, startZ, endX, endY, endZ, self.tmpPeekSpeed,
                            endTime - startTime)) # the last parameter is time duration of submovement

            self.tmpPeekSpeed = 0  # only a temporary variability,initized as 0 for the next submovement
            index = index + 1  # the start of next submovement begins after the end




    # index means the current index of frameArray
    # the loop begins with current index
    # return the start index of next submovement

    def getSubmovementStart(self,index):

        sumDuration=0

        for i in range(index,self.numberFrame):

            if sumDuration >= 100: # speed >0 up to 100 ms
                return i

            curFrame=self.frameArray[i]
            curTimeStamp=float(curFrame[colNumSplitTimestamp])
            duration=0

            if i!=0: # if i==0 prevFrame equals to curFrame
                prevFrame=self.frameArray[i-1]
                prevTimeStamp=float(prevFrame[colNumSplitTimestamp])
                duration=curTimeStamp-prevTimeStamp

            curSpeed=float(curFrame[colNumSplitSpeed])

            if curSpeed>self.pauseMarginSpeed:
                sumDuration+=duration

        return -1 # not found

    # return the acceleration speed of the current index
    def calculateAccelerationSpeed(self, index):

        prevFrame = self.frameArray[index - 1]
        prevTimeStamp = float(prevFrame[colNumSplitTimestamp])
        prevSpeed = float(prevFrame[colNumSplitSpeed])

        curFrame = self.frameArray[index]
        curSpeed = float(curFrame[colNumSplitSpeed])
        curTimeStamp = float(curFrame[colNumSplitTimestamp])

        curDuration = curTimeStamp - prevTimeStamp  # the duration between the prevSpeed and the curSpeed
        curAcc = (curSpeed - prevSpeed) / (
        curDuration + 0.0)  # the acceleration speed equals to the difference of curSpeed and prevSpeed divided by the time duration

        return curAcc


    # index means the current index of frame
    # judge if the submovement ends
    # there are three cases:
    # firstly,pause
    # secondly,acceleration speed changes from negtive to positive and the current speed < 75% of peek speed
    # thirdly,the negtive acceleration speed reached its relative max value
    def getSubmovementEnd(self,index):

        prevAcc = 0
        maxAcc = 0 # the max of absolute acc
        negtiveDuration=0 # record how many times continuous negtive acc occurs

        if index > 1:  # if index<=1,there will be no frameArray[index-2],so there will be no prevAcc. Thus,the second situation is meaningless
            prevAcc = self.calculateAccelerationSpeed(index - 1) # the initial value for prevAcc

        for j in range(index,self.numberFrame): # go through the remaining frames

            curFrame = self.frameArray[j]
            curSpeed = float(curFrame[colNumSplitSpeed])
            if curSpeed>self.tmpPeekSpeed:
                self.tmpPeekSpeed=curSpeed
            curAcc = self.calculateAccelerationSpeed(j)

            # first situation: pause( the speed is almost zero)
            if curSpeed < self.pauseMarginSpeed:
                return j

            # second situation
            if index>1 :
                # if index<=1,there will be no prevAcc,so the second situation is meaningless
                # acceleration speed change from negtive to positive and the current speed < 75% of peek speed
                if prevAcc<0 and curAcc>0 and curSpeed < 0.75*self.tmpPeekSpeed:
                    return j

            # the third situation,reach a relative max negtive acc
            # sudden brake
            # relative max means larger than the previous maximum and the next two frame
            if negtiveDuration>0:
                # if the curAcc reaches maximum, it should > prevAcc and also > nextAcc
                if abs(curAcc)>maxAcc and abs(curAcc)>self.brakeMarginAcc:
                    if j<self.numberFrame-1: # the last two does not have next two frame
                        nextAcc=self.calculateAccelerationSpeed(j+1)
                        if nextAcc>0: # the current acc is the max negative acceleration speed because the next acc becomes positive
                            return j

                        if abs(curAcc)>abs(nextAcc): # the current acc is the max negative acceleration speed
                            return j
                    else:
                        return j

            if abs(curAcc) > maxAcc:
                maxAcc = abs(curAcc) # update the max acc

            if curAcc >= 0:
                negtiveDuration = 0
                maxAcc=0
            else:
                negtiveDuration = negtiveDuration + 1

            prevAcc=curAcc

        return self.numberFrame-1 # if no ends are found, return the end of the frame

    def getTotalNumOfSubMovement(self):
        return len(self.submovement_list)

    # the verification time is the duration from the end of last submovement to the end of the trial
    def getVerificatonTime(self):

        endSubmovement=self.submovement_list[len(self.submovement_list)-1]
        endTime=endSubmovement.endTime
        self.verificationTime=self.finalLiftUpTime-endTime
        return self.verificationTime


    '''
    # not used now
    # measure the distribution of submovement endpoints in space
    # let the target point be the center,the target axis be the x axis
    # let the line vertical to x axis in the ipad plane be y axis
    # let the line vertical to the ipad plane be z axis
    # let the finger point be p ,the ipad plane be A, the line passing though p and vertical to A be l1
    # let the intersaction point of l1 and A be c
    # the z value is the distance between A and p.It's always positive since the finger can not go through the ipad
    # let the line segment passing target and c be l2
    # the intersection angle of l2 and target axis is a
    # the x value in the relative cooradinate is len(l2)*cos(a)
    # the y value in the relative cooradinate is len(l2)*sin(a)
    # return the relative cors of the current point
    def getRelativeCors(self,curX,curY,curZ):
        startFrame=self.frameArray[0] # the center of the axis
        startX=startFrame[self.colNumX]
        startY=startFrame[self.colNumY]
        startZ=startFrame[self.colNumZ]
        # get c in 3D cors
        cX,cY,cZ=getIntersactionPointOfLineAndPlane(curX,curY,curZ,self.targetX,self.targetY,self.targetZ)
        newX,newY=getRelativeXandY(curX,curY,curZ,startX,startY,startZ,self.targetX,self.targetY,self.targetZ)
        newZ = calculate_3D_Dis_Of_Two_Points(curX, curY, curZ, cX, cY, cZ)
        return newX,newY,newZ
    '''
    '''
    # the meaning of coincidentError is unsure now.
    # the perperdicular error is replaced by ME in Mackenzie's paper
    # return the coincidentErrorValue,coincidentErrorType and perpendicular error
    def calculateErrors(self,endpointX,endpointY,endpointZ):
        startFrame=self.frameArray[0]
        startX=startFrame[self.colNumX]
        startY=startFrame[self.colNumY]
        startZ=startFrame[self.colNumZ]
        dis=calculate_3D_Dis_Of_Two_Points(endpointX,endpointY,endpointZ,startX,startY,startZ) # the distance between the endpoint and start
        # the angle of l and target axis
        sinA,cosA=getIntersactionAngleOfTwoLines(endpointX,endpointY,endpointZ,startX,startY,startZ,startX,startY,startZ,self.targetX,self.targetY,self.targetZ)
        disAlong=dis*cosA # the distance along the target axis
        disVeticle=dis*sinA # the distance of the point to the line

        if (endpointX-startX)*(self.targetX-startX)<0: # the end point is in the negetive direction of ITA
            disAlong=(-1)*disAlong
        b=abs(self.targetX-startX) # the distance from start to the target
        concidentErrorValue=disAlong-b
        if concidentErrorValue>0:
            concidentErrorType="overshoot"
        else:
            # undershoot: |a-b|<b -> b-a<b -> a>0
            if disAlong>0:
                concidentErrorType="undershoot"
            else:
                concidentErrorType="counterproductive submovement"
        return concidentErrorValue,concidentErrorType
    '''



'''       
# this function is not used any more       
# for all trials in one experiment,get the percentage of trials contaning pauses
def calculatePercentageContainingPause(pid):
    files = os.listdir(path2)
    numOfFileWithPause=0 # how many files contain pause
    numOfFiles=0 # how many files of pid in total
    print 'file','pauseTime'
    # PID_xxx_Block_xxx_Trial_xxx.csv
    for file in files:  # open all the file in the '/split' directory
        if not os.path.isdir(file):  # not a directory
            # a bug : if the pid is 888,files begin with pid 8881 will be taken into account
            keys = file.split('_')
            if str(pid) in keys:  # if the file begins with PID_xxx
                numOfFiles=numOfFiles+1
                leap=LeapAnalyzerHuang(path2+file,pid)
                leap.loadLeapData()
                leap.calculateNumberOfFrame()
                leap.calculatePauseTime()
                print file,leap.pauseTime
                if leap.pauseTime>0:
                    numOfFileWithPause=numOfFileWithPause+1
    percentages=numOfFileWithPause/(numOfFiles+0.0) # avoid divide integer error
    return percentages
'''

'''
def test_submovement():
    pid = 891
    block=1
    trial=4
    readfile=path2+'PID_'+str(pid)+'_Block_'+str(block)+'_Trial_'+str(trial)+'.csv'
    leap=LeapAnalyzerHuang(readfile,pid,block,trial)
    leap.loadLeapData()
    leap.getSubmovements()
    print 'submovements'
    print 'startTime','endTime','peekSpeed','duration'
    for  s in leap.submovement_list:
        print s.startTime,s.endTime,s.peekSpeed,s.duration
    print 'totalNumOfSubMovement', leap.getTotalNumOfSubMovement()
    print 'verifcation time(mm)',leap.getVerificatonTime()
    numBeforeFinal,numSlipOff=leap.getNumOfSubmovementInTwoSets()
    print 'numOfSubmovementsBeforeFinal',numBeforeFinal
    print 'numOfSubmovementSlipOff',numSlipOff
    
'''

#print "percentage of pause"
#print calculatePercentageContainingPause(pid)
#test_submovement()


