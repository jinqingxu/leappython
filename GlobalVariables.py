# used to store global variables that are used in many scripts
import math
import csv
import time
# the index of data in android file
offsetAndroidStartTime = 11
offsetAndroidFinalLiftUp = 24
offsetAndroidBlock=2
offsetAndroidTrial=3
offsetAndroidAmplitude=5
offsetAndroidWidth=7
offsetAndroidWidthInPixel=6
offsetAndroidDirection=8
offsetAndroidTargetX=12
offsetAndroidTargetY=13
offsetAndroidFirstLiftUpX=16
offsetAndroidFirstLiftUpY=17
offsetAndroidFirstTouchDownX=14
offsetAndroidFirstTouchDownY=15


# the index of data in leap file
offsetLeapX=3
offsetLeapY=4
offsetLeapZ=5


#workpath
pathheader = '/Users/irene/Documents/McGillUni/ACT_Research_Lab/Experiments/Motion Tracking Study/Experiment Data/'

#path2 = pathheader+"split/"

# index of the data from split files
offsetSplitX = 9
offsetSplitY = 10
offsetSplitZ = 11
offsetSplitTimestamp = 8
offsetSplitSpeedX = 21
offsetSplitSpeedY = 22
offsetSplitSpeedZ = 23
offsetSplitWidth = 4
offsetSplitSpeed=24
offsetSplitDirection=5
offsetSplitAmplitude=3

# the index of data in dif file
offsetDisBlock=0
offsetDisTrial=1
offsetDisAmplitude=2
offsetDisWidth=3
offsetDisDirection=4
offsetDisDistance=7
offsetDisDifference=8
offsetDisAbsDifference=9

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

# locations measured by leap motion
startLeap3DX=3.42
startLeap3DY=58.42
startLeap3DZ=-75.76

# the offset of the start measured by leap motion relative to the real position is x,y,z
offset3DX=start3DX-startLeap3DX
offset3DY=start3DY-startLeap3DY
offset3DZ=start3DZ-startLeap3DZ

# input a pid
# output the offsetX,offsetY,offsetZ of the nearest experiment before PID_XXX
def getOffetXYZ(pid):

    readfile=pathheader+'PID_'+pid+'/'+"PID_"+str(pid)+"_Data_from_LEAPtest_results_Frame.csv"

    # get the dateTime of the target select experiment
    with open(readfile) as f:

        f_csv = csv.reader(f)
        i=0
        dateTimeStr=""
        for row in f_csv:
            if i==1: # date
                dateList=row.Split(':')
                dateList2=dateList[1].strip().split('/') # demo value: 2017 09 30  use strip to remove space
                dateTimeStr=dateList2[0]+'-'+dateList2[1]+'-'+dateList2[2]
            if i==2: # time
                timeStr=row[5:len(row)]
                dateTimeStr+=timeStr
            i=i+1
            if i>=3:
                break

        dateTimeTargetSelect=time.strptime(dateTimeStr, "%Y-%m-%d %H:%M:%S")
        print(dateTimeTargetSelect)







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


