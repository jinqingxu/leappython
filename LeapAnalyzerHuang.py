# the measures from huang's paper
import numpy as np
import matplotlib.pyplot as plt
import csv
import math
import os
import matplotlib.pyplot as plt
# import helper functions from other script
from CalculateOfCircle import get_min_max_mean_deviation_from_list
from SpaceUtils import calculate_3D_Dis_Of_Two_Points
from SpaceUtils import getIntersactionPointOfLineAndPlane
from SpaceUtils import getRelativeXandY
from SpaceUtils import getIntersactionAngleOfTwoLines
path = "/Users/irene/Documents/McGillUni/ACT_Research_Lab/Experiments/Motion Tracking Study/Experiment Data/split/"
path2="/Users/irene/Documents/McGillUni/ACT_Research_Lab/Experiments/Motion Tracking Study/Experiment Data/"
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
    relaendX=0
    relaendY=0
    relaendZ=0
    coincidentErrorValue=0
    coincidentErrorType=""
    perpendicularError=0
    '''
    def __init__(self,startTime,endTime,startX,startY,startZ,endX,endY,endZ,peekSpeed,duration):
        self.startTime=startTime
        self.endTime=endTime
        self.startX=startX
        self.startY=startY
        self.startZ=startZ
        self.endX=endX
        self.endY=endY
        self.endZ=endZ
        self.peekSpeed=peekSpeed
        self.duration=duration
        '''
        self.relaendX=relaendX
        self.relaendY=relaendY
        self.relaendZ=relaendZ
        self.coincidentErrorValue=coincidentErrorValue
        self.coincidentErrorType=coincidentErrorType
        '''


class LeapAnalyzerHuang:
    pid=0
    readFile=""
    frameArray=[]
    numberFrame=0
    peekSpeed=0
    pauseTime=0
    pauseDuration=[]
    pauseLocation=[]
    pauseMarginSpeed=0.01 # due to the measure mistake of leap motion,the pauseMargin should not be 0
    brakeMarginAcc=1
    submovement_list=[]
    width=0
    # store target data,initialized in the loaddata function
    targetX=0
    targetY=0
    targetZ=0
    targetTime=0
    RelativeEndCors=[] # store the 3D points of end of submovements
    verificationTime=0.0 # the verification time,the duration from the end of the last submovement to the end of the trial

    def __init__(self,readFile,pid):
        self.readFile=readFile
        self.pid=pid

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
            next(f_csv) # skip the header
            for row in f_csv:
                self.frameArray.append(row)
        self.numberFrame = len(self.frameArray)
        firstFrame=self.frameArray[0]
        self.width=float(firstFrame[self.offsetWidth])
        targetFrame=self.frameArray[self.numberFrame-1]
        self.targetX=float(targetFrame[self.offsetX])
        self.targetY=float(targetFrame[self.offsetY])
        self.targetZ=float(targetFrame[self.offsetZ])
        self.targetTime=float(targetFrame[self.offsetTimestamp])


    def calculateNumberOfFrame(self):
        return self.numberFrame

    # let the finger point be p ,the laptop plane be A, the line passing though p and vertical to A be l
    # let the intersaction of l and A be c
    # spiral should meet two conditions
    # firstly, c should be inside the target
    # secondly,the distance between p and A should be very small
    def judgeInsideTarget(self, curX, curY, curZ, targetX, targetY, targetZ, width):
        margin = 15  # the max distance of p and A
        # since the angle of the laptop is 45 degree,the normal vector of the laptop plane is (0,1,1)
        # so the function of line l is (x-curX)/0=(y-curY)/1=(z-curZ)/1 ,that is y-curY=z-curZ=k
        # let y=curY+k,z=curZ+k
        # the function of the laptop is 0*(x-targetX)+1*(y-targetY)+1*(z-targetZ)=0
        # put y and z into the laptop function
        # k=(targetY+targetZ-curY-curZ)/2
        # so y=curY+k=(targetY+targetZ+curY-curZ)/2
        # z=curZ+k=(targetY+targetZ+curZ-curY)/2
        # x=curX
        intersactionX = curX
        intersactionY = (targetY + targetZ + curY - curZ) / 2
        intersactionZ = (targetY + targetZ + curZ - curY) / 2
        # find the distance between p and A
        dis = calculate_3D_Dis_Of_Two_Points(curX, curY, curZ, intersactionX, intersactionY, intersactionZ)
        if dis > margin:
            return False
        else:  # dis should be smaller or equal to margin
            dis2 = calculate_3D_Dis_Of_Two_Points(targetX, targetY, targetZ, intersactionX, intersactionY,
                                                  intersactionZ)
            if dis2 > width:
                return False
            else:
                return True

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
    # no return value
    # change the value of self.pauseTime,self.pauseDuration
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
                        nextSpeed=float(nextFrame[self.offsetSpeed])
                        if self.judgePause(nextSpeed) == False:
                            endTime = float(nextFrame[self.offsetTimestamp])
                            duration = endTime - startTime
                            self.pauseDuration.append(duration)
                            i=j
                            break
            i=i+1


    # get number of submovements before final entry
    # be inside the target but before lift up
    # alsp get number of submovements slip off
    # return numBeforeFinal,numSlipOff
    def getNumOfSubmovementInTwoSets(self):
        numBeforeFinal=0
        numSlipOff=0
        for s in self.submovement_list:
            if self.judgeInsideTarget(s.startX,s.startY,s.startZ,self.targetX,self.targetY,self.targetZ,self.width)==True: # the start of the submovement is inside the target
                if self.judgeInsideTarget(s.endX,s.endY,s.endZ,self.targetX,self.targetY,self.targetZ,self.width)==True: # before the final entry
                    numBeforeFinal=numBeforeFinal+1
                else: # the start is inside the target,the end is outside the target.That means slip off
                    numSlipOff=numSlipOff+1
        return numBeforeFinal,numSlipOff




    # record the pause location
    # append it in the pauseLoction
    # the location means the distance between the current location and the target
    def calculatePauseLocation(self,curX,curY,curZ):
        dis=calculate_3D_Dis_Of_Two_Points(curX,curY,curZ,self.targetX,self.targetY,self.targetZ)
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
            startIndex=offset
            startTime=float(self.frameArray[startIndex][self.offsetTimestamp])
            startX=float(self.frameArray[startIndex][self.offsetX])
            startY=float(self.frameArray[startIndex][self.offsetY])
            startZ=float(self.frameArray[startIndex][self.offsetZ])
            if startIndex==-1: # there is no submovements int the future
                break
            offset=self.getSubmovementEnd(offset+1) # after the start
            endIndex=offset
            endX=float(self.frameArray[endIndex][self.offsetX])
            endY=float(self.frameArray[endIndex][self.offsetY])
            endZ=float(self.frameArray[endIndex][self.offsetZ])
            endTime=float(self.frameArray[endIndex][self.offsetTimestamp])
            #relaendX,relaendY,relaendZ=self.getRelativeCors(endX,endY,endZ)
            #coincidentErrorValue,coincidentErrorType=self.calculateCoincidentError(endX)
            self.submovement_list.append(SubMovement(startTime,endTime,startX,startY,startZ,endX,endY,endZ,self.peekSpeed,endTime-startTime))
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

    # the verification time is the duration from the end of last submovement to the end of the trial
    def getVerificatonTime(self):
        endSubmovement=self.submovement_list[len(self.submovement_list)-1]
        endTime=endSubmovement.endTime
        self.verificationTime=self.targetTime-endTime
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
        startX=startFrame[self.offsetX]
        startY=startFrame[self.offsetY]
        startZ=startFrame[self.offsetZ]
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
        startX=startFrame[self.offsetX]
        startY=startFrame[self.offsetY]
        startZ=startFrame[self.offsetZ]
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
    # go through all the trials in one experiment
    # draw targets and each first lift up points
    # the target is represented with green color
    # where the lift up points are represented with red color
    def drawTargetFirstLiftUpPlot2D(self):
        file=path2+"PId_"+str(self.pid)+"_TwoDFittsData_External.csv"
        targetX_list=[]
        targetY_list=[]
        liftUpX_list=[]
        liftUpY_list=[]
        offsetTargetX=12
        offsetTargetY=13
        offsetLiftUpX=16
        offsetLiftUpY=17
        with open(file) as f:
            f_csv = csv.reader(f)
            for i in range(0, 9):  # skip the beginning
                next(f_csv)
            headers = next(f_csv)  # get headers of csv
            for row in f_csv:
                targetX_list.append(float(row[offsetTargetX]))
                targetY_list.append(float(row[offsetTargetY]))
                liftUpX_list.append(float(row[offsetLiftUpX]))
                liftUpY_list.append(float(row[offsetLiftUpY]))
            # draw the picture
            plt.title('distribution of First attempt')
            plt.scatter(targetX_list, targetY_list, c='c', alpha=1, marker='o', label='target', s=100,
                            edgecolors='black')
            plt.scatter(liftUpX_list, liftUpY_list, c='r', alpha=1, marker='o', label='First_Lift_Up', s=30,
                            edgecolors='black')
            plt.xlabel('First Lift Up X(pixel)')
            plt.ylabel('First Left Up Y(pixel)')
            plt.legend()
            plt.grid(True)
            plt.show()


    def drawRelativeTargetFirstLiftUpPlot2D(self,block,trial):
        file = path2 + "PId_" + str(self.pid) + "_TwoDFittsData_External.csv"
        targetX_list = []
        targetY_list = []
        liftUpX_list = []
        liftUpY_list = []
        offsetTargetX = 12
        offsetTargetY = 13
        offsetLiftUpX = 16
        offsetLiftUpY = 17
        with open(file) as f:
            f_csv = csv.reader(f)
            for i in range(0, 9):  # skip the beginning
                next(f_csv)
            headers = next(f_csv)  # get headers of csv
            for row in f_csv:
                if int(row[2])==block and int(row[3])==trial:
                    targetX=float(row[offsetTargetX])
                    targetY=float(row[offsetTargetY])
                    targetX_list.append(0)
                    targetY_list.append(0)
                    liftUpX=float(row[offsetLiftUpX])
                    liftUpY=float(row[offsetLiftUpY])
                    relaLiftUpX=liftUpX-targetX
                    relaLiftUpY=liftUpY-targetY
                    liftUpX_list.append(relaLiftUpX)
                    liftUpY_list.append(relaLiftUpY)
                    break
            # draw the picture
            plt.title('distribution of First attempt relative to the target in single trial')
            plt.scatter(targetX_list, targetY_list, c='c', alpha=1, marker='o', label='target', s=100,
                                edgecolors='black')
            plt.scatter(liftUpX_list, liftUpY_list, c='r', alpha=1, marker='o', label='First_Lift_Up', s=30,
                                edgecolors='black')
            margin=40 # the margin of the plot
            plt.xlim((-1 * (targetX_list[0]+margin), targetX_list[0]+margin))
            plt.ylim((-1 * (targetY_list[0]+margin), targetY_list[0]+margin))
            plt.xlabel('First Lift Up X(pixel)')
            plt.ylabel('First Left Up Y(pixel)')
            plt.legend()
            plt.grid(True)
            plt.show()


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
    readfile=path+'PID_890_Block_1_Trial_4.csv'
    pid=901
    leap=LeapAnalyzerHuang(readfile,pid)
    '''
    leap.loadLeapData()
    leap.getSubmovements()
    for  s in leap.submovement_list:
        print s.startTime,s.endTime,s.peekSpeed,s.duration
    print 'totalNumOfSubMovement', leap.getTotalNumOfSubMovement()
    print 'verifcation time(mm)',leap.getVerificatonTime()
    numBeforeFinal,numSlipOff=leap.getNumOfSubmovementInTwoSets()
    print 'numOfSubmovementsBeforeFinal',numBeforeFinal
    print 'numOfSubmovementSlipOff',numSlipOff
    '''
    #leap.drawTargetFirstLiftUpPlot2D()
    leap.drawRelativeTargetFirstLiftUpPlot2D(1,6)


test_submovement()

