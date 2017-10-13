# used to store global variables that are used in many scripts
import math
import csv
import time

#workpath
pathHeader='/Users/irene/Documents/McGillUni/ACT_Research_Lab/Experiments/Motion Tracking Study/'
pathHeaderForData = pathHeader+'Experiment Data/'
pathHeaderForIndividual=pathHeader+'All Individual Experiment Result/'
pathHeaderForAllOldAdults=pathHeader+'All Old Adults Experiment Result/'
pathHeaderForAllYoungAdults=pathHeader+'All Young Adults Experiment Result/'
pathHeaderForAllParticipiants=pathHeader+'All Participants Experiment Result/'
pathHeaderForAccuracy=pathHeader+'Leap Accuracy/'
pathHeaderForCrossHair=pathHeaderForAccuracy+'CrossHair Data/'
pathHeaderForPrecision=pathHeaderForAccuracy+'Precision Data/'

# the column number of data in android file
colNumAndroidStartTime = 17
colNumAndroidFinalLiftUp = 24
colNumAndroidBlock=2
colNumAndroidTrial=3
colNumAndroidAmplitude=5
colNumAndroidWidth=7
colNumAndroidWidthInPixel=6
colNumAndroidDirection=8
colNumAndroidTargetX=11
colNumAndroidTargetY=12
colNumAndroidFirstLiftUpX=15
colNumAndroidFirstLiftUpY=16
colNumAndroidFirstTouchDownX=13
colNumAndroidFirstTouchDownY=14
colNumAndroidFirstLiftUpTimeStamp=20

# the index of data in leap file
colNumLeapX=3
colNumLeapY=4
colNumLeapZ=5
colNumLeapTimeStamp=2

# index of the data from split files
colNumSplitX = 9
colNumSplitY = 10
colNumSplitZ = 11
colNumSplitTimestamp = 8
colNumSplitSpeedX = 21
colNumSplitSpeedY = 22
colNumSplitSpeedZ = 23
colNumSplitWidth = 4
colNumSplitSpeed=24
colNumSplitDirection=5
colNumSplitAmplitude=3

# the index of data in dif file
colNumDisBlock=0
colNumDisTrial=1
colNumDisAmplitude=2
colNumDisWidth=3
colNumDisDirection=4
colNumDisDistance=7
colNumDisDifference=8
colNumDisAbsDifference=9

# pixel to mm
# 1 pixel = 0.0794 mm(calculated by Irene)
# 1 pixel = 0.088194mm(from the website)
PixelToM=0.088194
Pi=3.1415926

# 3D point
class ThreeCorPoint:
    x=0
    y=0
    z=0
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

# 2D point
class TwoCorPoint:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 3D coordinates for the start button
# measured by ruler
start3DX=0
start3DY=50
start3DZ=-85

# 2D coordinates for the start button
# in pixel
start2DX=1024
start2DY=695

# start point in 2D
startThreeCor=ThreeCorPoint(start3DX,start3DY,start3DZ)
startTwoCor=TwoCorPoint(start2DX,start2DY)

# the angle of the tablet
tabletAngle=45

# the normal vector of the tablet
normalVectorX=0
normalVectorY=1
normalVectorZ=1

# input a pid
# output the offsetX,offsetY,offsetZ of the nearest experiment before PID_XXX
def getOffetXYZ(pid):
    if float(pid) < 200:
        readfile = pathHeaderForData + 'Old Adults/' + 'PID_' + str(pid) + '/' + "PID_" + str(
            pid) + "_Data_from_LEAPtest_results_Frame.csv"
    else:
        readfile = pathHeaderForData + 'Young Adults/' + 'PID_' + str(pid) + '/' + "PID_" + str(
            pid) + "_Data_from_LEAPtest_results_Frame.csv"
    dateTimeTargetSelect,dateTimeTargetSelectStr=getDateTimeForLeapData(readfile)
    # find the nearest timestamp

    #startPointFile=pathHeaderForData+'Records_Of_StartButton_Offset.csv'
    startPointFile = pathHeaderForCrossHair + 'Average_x_y_z_of_crossHair_experiment.csv'

    with open(startPointFile) as f:

        f_csv = csv.reader(f)
        next(f_csv) # skip the header
        i=0
        for row in f_csv:
            if len(row[1]) < 19:  # sometimes the datetime will be like 2017-09-13 12:12 it should be 12:12:00 to satisfy the date format
                row[1] += ':00'

            if i==0:
                prevDateTimeStart = time.strptime(row[1], "%Y-%m-%d %H:%M:%S")
                prevStartX = float(row[2])
                prevStartY = float(row[3])
                prevStartZ = float(row[4])

            dateTimeStartPoint=time.strptime(row[1], "%Y-%m-%d %H:%M:%S")
            if dateTimeStartPoint > dateTimeTargetSelect: # choose the prevDateTime which is earlier than the current dateTime
                return prevStartX-start3DX,prevStartY-start3DY,prevStartZ-start3DZ

            prevDateTimeStart = time.strptime(row[1], "%Y-%m-%d %H:%M:%S")
            prevStartX = float(row[2])
            prevStartY = float(row[3])
            prevStartZ = float(row[4])

            i=i+1
        # if no crossHair experiments are taken after this target select experiment, return the data of the last experiment
        return prevStartX-start3DX, prevStartY-start3DY, prevStartZ-start3DZ



def getDateTimeForLeapData(readfile):



    # get the dateTime of the target select experiment
    with open(readfile) as f:

        f_csv = csv.reader(f)

        i=0

        dateTimeStr=""

        for row in f_csv:

            if i==1: # date
                dateList=row[0].split(':')
                dateList2=dateList[1].strip().split('/') # demo value: 2017 09 30  use strip to remove space
                dateTimeStr=dateList2[0]+'-'+dateList2[1]+'-'+dateList2[2]
            if i==2: # time
                timeStr=row[0][5:len(row)-2]
                dateTimeStr+=' '
                dateTimeStr+=timeStr.strip()
            i=i+1
            if i>=3:
                break

        dateTime=time.strptime(dateTimeStr, "%Y-%m-%d %H:%M:%S")

        return dateTime,dateTimeStr

