# seven measures
import csv
import math
import os
from CalculateOfCircle import get_min_max_mean_deviation_from_list
from CalculateOfCircle import calculate_3D_Dis_Of_Two_Points

path = "/Users/irene/Documents/McGillUni/ACT_Research_Lab/Experiments/Motion Tracking Study/Experiment Data/split/"

class SubMovement:
    startIndex=0 # the start index of frame
    endIndex=0 # the end index of frame
    peekSpeed=0.0
    def __init__(self,startIndex,endIndex,peekSpeed):
        self.startIndex=startIndex
        self.endIndex=endIndex
        self.peekSpeed=peekSpeed


class LeapAnalyzerHuang:
    readFile=""
    frameArray=[]
    numberFrame=0
    peekSpeed=0
    pauseTime=0
    pauseDuration=[]
    pauseLocation=[]
    pauseMarginSpeed=0.5  # due to the measure mistake of leap motion,the pauseMargin should not be 0
    brakeMarginAcc=1
    submovement_list=[]

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

    offsetSpeed=24

    offsetWidth=4

    def loadLeapData(self):
        file = self.readFile
        with open(file) as f:
            f_csv = csv.reader(f)
            next(f_csv)
            for row in f_csv:
                self.frameArray.append(row)
        self.numberFrame = len(self.frameArray)

    def calculateNumberOfFrame(self):
        return self.numberFrame

    # the current speed is near zero
    def judgePause(self,speed):
        #if abs(speedX)<=self.pauseMargin and abs(speedY)<=self.pauseMargin and abs(speedZ)<=self.pauseMargin:
        if speed< self.pauseMarginSpeed:
            return True
        else:
            return False

    # for one trial,get the average pause duration
    # the unit of duration is ms
    def getMeanPauseDuration(self):
        minp, maxp, averagep, deviationp = get_min_max_mean_deviation_from_list(self.pauseDuration)
        return averagep

    #calculate the pause time and each pause duration
    def calculatePauseTime(self):
        i=0
        while i <self.numberFrame:
            curFrame=self.frameArray[i]
            #curspeedX=float(curFrame[self.offsetSpeedX])
            #curspeedY=float(curFrame[self.offsetSpeedY])
            #curspeedZ=float(curFrame[self.offsetSpeedZ])
            curSpeed=float(curFrame[self.offsetSpeed])
            startTime=float(curFrame[self.offsetTimestamp]) # the start time of the pause
            #if self.judgePause(curspeedX,curspeedY,curspeedZ)==True:
            if self.judgePause(curSpeed) == True:
                self.pauseTime=self.pauseTime+1
                curX=float(curFrame[self.offsetX])
                curY=float(curFrame[self.offsetY])
                curZ=float(curFrame[self.offsetZ])
                self.calculatePauseLocation(curX,curY,curZ)
                if i==self.numberFrame-1: # if the current frame is the end one
                    self.pauseDuration.append(0) # pause time is zero
                else:
                    for j in range(i + 1, self.numberFrame):
                        nextFrame = self.frameArray[j]
                        '''
                        nextspeedX = float(nextFrame[self.offsetSpeedX])
                        nextspeedY = float(nextFrame[self.offsetSpeedY])
                        nextspeedZ = float(nextFrame[self.offsetSpeedZ])
                        '''
                        nextSpeed=float(nextFrame[self.offsetSpeed])
                        if self.judgePause(nextSpeed) == False:
                            endTime = float(nextFrame[self.offsetTimestamp])
                            duration = endTime - startTime
                            self.pauseDuration.append(duration)
                            i=j
                            break
            i=i+1

    # record the pause location
    # append it in the pauseLoction
    # the location means the distance between the current location and the target
    def calculatePauseLocation(self,curX,curY,curZ):
        targetFrame = self.frameArray[self.numberFrame - 1]  # end frame represent the target
        targetX = float(targetFrame[self.offsetX])
        targetY = float(targetFrame[self.offsetY])
        targetZ = float(targetFrame[self.offsetZ])
        dis=calculate_3D_Dis_Of_Two_Points(curX,curY,curZ,targetX,targetY,targetZ)
        self.pauseLocation.append(dis)

    # return the acceleration speed of the current offset
    def calculateAccelerationSpeed(self,offset):
        prevFrame = self.frameArray[offset - 1]
        prevTimeStamp = float(prevFrame[self.offsetTimestamp])
        prevSpeed = float(prevFrame[self.offsetSpeed])
        curFrame=self.frameArray[offset]
        curSpeed=float(curFrame[self.offsetSpeed])
        curTimeStamp = float(curFrame[self.offsetTimestamp])
        curDuration = curTimeStamp - prevTimeStamp
        curAcc = (curSpeed-prevSpeed)/(curDuration+0.0)
        return curAcc


    # offset means the current index of frame
    # begin with current offset
    # return the start index of next submovement
    def getSubmovementStart(self,offset):
        sumDuration=0
        for i in range(offset,self.numberFrame):
            if sumDuration >= 100: # speed >0 up to 100 ms
                return i-1
            curFrame=self.frameArray[i]
            curTimeStamp=float(curFrame[self.offsetTimestamp])
            duration=0
            if i!=0: # if i==0 prevFrame equals to curFrame
                prevFrame=self.frameArray[i-1]
                prevTimeStamp=float(prevFrame[self.offsetTimestamp])
                duration=curTimeStamp-prevTimeStamp
            curSpeed=float(curFrame[self.offsetSpeed])
            if curSpeed>self.pauseMarginSpeed:
                sumDuration+=duration
        return -1

    # go through the self.Frames
    # find all submovements and put them into submovement_list
    def getSubmovements(self):
        offset=0
        while offset<self.numberFrame:
            offset=self.getSubmovementStart(offset) # the start index of the submovement
            start=offset
            offset=self.getSubmovementEnd(offset+1) # after the start
            end=offset
            self.submovement_list.append(SubMovement(start,end,self.peekSpeed))
            self.peekSpeed=0 # prepared for the next submovement
            offset=offset+1 # the start of next submovement begins after the end

    # curoffset means the current index
    # judge if the submovement ends
    # there are three cases:
    # firstly,pause
    # secondly,acceleration speed changes from negtive to positive and the current speed < 75% of peek speed
    # thirdly,the negtive acceleration speed reached its relative max value
    def getSubmovementEnd(self,offset):
        prevAcc = 0
        maxAcc = 0 # the max of absolute acc
        negtive=0 # record how many continuous negtive acc occurs
        if offset > 1:  # if offset<=1,there will be no grandFrame,so the second situation is meaningless
            prevAcc = self.calculateAccelerationSpeed(offset - 1)
        for j in range(offset,self.numberFrame):
            curFrame = self.frameArray[j]
            curSpeed = float(curFrame[self.offsetSpeed])
            if curSpeed>self.peekSpeed:
                self.peekSpeed=curSpeed
            curAcc = self.calculateAccelerationSpeed(j)
            # pause
            if curSpeed < self.pauseMarginSpeed:
                return j
            if offset>1 :
                # if curoffset<=1,there will be no grandFrame,so the second situation is meaningless
                # acceleration speed change from negtive to positive and the current speed < 75% of peek speed
                if prevAcc<0 and curAcc>0 and curSpeed < 0.75*self.peekSpeed:
                    return j
            # the third situation,reach a relative max negtive acc
            # sudden brake
            # relative max means larger than the previous maximum and the next two frame
            if negtive>0:
                if abs(curAcc)>maxAcc and abs(curAcc)>self.brakeMarginAcc:
                    if j<self.numberFrame-2: # the last two does not have next two frame
                        nextAcc=self.calculateAccelerationSpeed(j+1)
                        nextNextAcc=self.calculateAccelerationSpeed(j+2)
                        if abs(curAcc)>abs(nextAcc) and abs(curAcc)>abs(nextNextAcc):
                            return j
                    else:
                        return j
            if abs(curAcc) > maxAcc:
                maxAcc = abs(curAcc)
            if curAcc >= 0:
                negtive = 0
            else:
                negtive = negtive + 1
            prevAcc=curAcc
        return self.numberFrame-1

    def getTotalNumOfSubMovement(self):
        return len(self.submovement_list)

# for all trials in one experiment,get the percentage of trials contaning pauses
def calculatePercentageContainingPause(pid):
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
                leap=LeapAnalyzerHuang(path+file)
                leap.loadLeapData()
                leap.calculateNumberOfFrame()
                leap.calculatePauseTime()
                print file,leap.pauseTime,leap.calculatePauseTime()
                if leap.pauseTime>0:
                    numOfFileWithPause=numOfFileWithPause+1
    percentages=numOfFileWithPause/(numOfFiles+0.0) # avoid divide integer error
    return percentages

pid=885
#print "percentage of pause"
#print calculatePercentageContainingPause(pid)

def test_submovement():
    readfile=path+'PID_885_Block_1_Trial_4.csv'
    leap=LeapAnalyzerHuang(readfile)
    leap.loadLeapData()
    leap.getSubmovements()
    for  s in leap.submovement_list:
        print s.startIndex,s.endIndex,s.peekSpeed
    print 'totalNumOfSubMovement', leap.getTotalNumOfSubMovement()


test_submovement()


