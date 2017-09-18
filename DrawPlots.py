# this function is used to draw plots
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import csv
import math
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from GlobalVariables import startThreeCor
from GlobalVariables import  offset3DX
from GlobalVariables import  offset3DY
from GlobalVariables import offset3DZ
# import helper functions from other script

from GlobalVariables import path2
from GlobalVariables import offsetSplitX
from GlobalVariables import  offsetSplitY
from GlobalVariables import offsetSplitZ
from GlobalVariables import  offsetSplitTimestamp
from GlobalVariables import offsetSplitDirection
from GlobalVariables import  offsetSplitAmplitude
from GlobalVariables import offsetAndroidBlock
from GlobalVariables import offsetAndroidTrial
from GlobalVariables import  offsetAndroidTargetX
from GlobalVariables import  offsetAndroidTargetY
from GlobalVariables import offsetAndroidFirstLiftUpX
from GlobalVariables import  offsetAndroidFirstLiftUpY
from GlobalVariables import PixelToM
from GlobalVariables import startThreeCor
from FileUtils import getSortedSplitFile
from GlobalVariables import path
from GlobalVariables import offsetSplitWidth
from SpaceUtils import getTargetLocationFor3DWithDirection
from  SpaceUtils import  getTargetLocationFor3D
from GlobalVariables import ThreeCorPoint

# used for draw plots of path
class FingerPath:
    # the start point of the path
    StartPathX=[]
    StartPathY=[]
    StartPathZ=[]
    # the end point of the path
    EndPathX=[]
    EndPathY=[]
    EndPathZ=[]
    # the points in the  intermediate path
    InterPathX=[]
    InterPathY=[]
    InterPathZ=[]

    def __init__(self,StartPathX,StartPathY,StartPathZ,EndPathX,EndPathY,EndPathZ,InterPathX,InterPathY,InterPathZ):
        self.StartPathX=StartPathX
        self.StartPathY=StartPathY
        self.StartPathZ=StartPathZ
        self.EndPathX=EndPathX
        self.EndPathY=EndPathY
        self.EndPathZ=EndPathZ
        self.InterPathX=InterPathX
        self.InterPathY=InterPathY
        self.InterPathZ=InterPathZ




class DrawPlots:
    pid = 0
    block = 0
    trial = 0
    readFile = ""
    frameArray = []
    numberFrame = 0
    # store target data,initialized in the loaddata function
    targetX = 0
    targetY = 0
    targetZ = 0
    direction=0
    startPathThreeCor=0
    endPathThreeCor=0
    width=0
    amplitude=0

    def __init__(self,pid):
        self.pid=pid
        self.frameArray = []
        self.numberFrame = 0

    def loadLeapData(self):
        file = self.readFile
        self.frameArray = []
        with open(file) as f:
            f_csv = csv.reader(f)
            next(f_csv)  # skip the header
            for row in f_csv:
                self.frameArray.append(row)
        self.numberFrame = len(self.frameArray)
        firstFrame = self.frameArray[0]
        self.width = float(firstFrame[offsetSplitWidth])
        targetFrame = self.frameArray[self.numberFrame - 1]
        targetThreeCor = getTargetLocationFor3D(self.pid, self.block,
                                                self.trial)  # with accurate start coordinate in 3D,calculate the target 3D
        self.targetX = targetThreeCor.x
        self.targetY = targetThreeCor.y
        self.targetZ = targetThreeCor.z
        self.targetTime = float(targetFrame[offsetSplitTimestamp])
        self.direction=float(self.frameArray[0][offsetSplitDirection])
        # the start of the path is the first frame
        # construct a three-cor class with x,y and z
        self.startPathThreeCor=ThreeCorPoint(float(self.frameArray[0][offsetSplitX]),float(self.frameArray[0][offsetSplitY]),float(self.frameArray[0][offsetSplitZ]))
        self.endPathThreeCor=ThreeCorPoint(float(self.frameArray[self.numberFrame-1][offsetSplitX]),float(self.frameArray[self.numberFrame-1][offsetSplitY]),float(self.frameArray[self.numberFrame-1][offsetSplitZ]))
        self.amplitude=float(self.frameArray[0][offsetSplitAmplitude])


    # go through all the trials in one experiment
    # draw targets and each first lift up points
    # the target is represented with green color
    # where the lift up points are represented with red color
    def drawTargetFirstLiftUpPlot2D(self):
        file = path + "PId_" + str(self.pid) + "_TwoDFittsData_External.csv"
        targetX_list = []
        targetY_list = []
        liftUpX_list = []
        liftUpY_list = []
        with open(file) as f:
            f_csv = csv.reader(f)
            for i in range(0, 10):  # skip the beginning
                next(f_csv)
            for row in f_csv:
                targetX_list.append(float(row[offsetAndroidTargetX]) * PixelToM)  # change from Pixel to mm
                targetY_list.append(float(row[offsetAndroidTargetY]) * PixelToM)
                liftUpX_list.append(float(row[offsetAndroidFirstLiftUpX]) * PixelToM)
                liftUpY_list.append(float(row[offsetAndroidFirstLiftUpY]) * PixelToM)
            # draw the picture
            plt.title('distribution of First attempt')
            plt.scatter(targetX_list, targetY_list, c='c', alpha=1, marker='o', label='Target', s=100,
                        edgecolors='black')
            plt.scatter(liftUpX_list, liftUpY_list, c='r', alpha=1, marker='o', label='FLU', s=30,
                        edgecolors='black')
            plt.xlabel('First Lift Up X(mm)')
            plt.ylabel('First Left Up Y(mm)')
            plt.legend()
            plt.grid(True)
            plt.show()

    # find the First Lift Up Cors in leap motion
    # find the closest timestamp
    def getFirstLiftUpCors(self, FirstLiftUpTimestamp):
        for i in range(len(self.frameArray)):
            curTime = float(self.frameArray[i][offsetSplitTimestamp])
            if curTime == FirstLiftUpTimestamp:
                return i
            if curTime > FirstLiftUpTimestamp:
                prev = float(self.frameArray[i - 1][offsetSplitTimestamp])
                if abs(prev - FirstLiftUpTimestamp) < abs(curTime - FirstLiftUpTimestamp):  # find the closest one
                    return i - 1
                else:
                    return i
        return len(self.frameArray) - 2  # if not found,the one before final LiftUp is the end of the submovement

    # the distribution of lift up in the first attempt
    def drawTargetFirstLiftUpPlot3D(self):
        fileandroid = path + "PId_" + str(self.pid) + "_TwoDFittsData_External.csv"
        firstLiftUpTime_list = []
        offsetFirstLiftUp = 20
        # store 3D cors for target
        targetX_list = []
        targetY_list = []
        targetZ_list = []
        # store 3D cors for first lift up
        firstLiftUpX_list = []
        firstLiftUpY_list = []
        firstLiftUpZ_list = []
        with open(fileandroid) as f:
            f_csv = csv.reader(f)
            for i in range(0, 10):  # skip the beginning
                next(f_csv)
            for row in f_csv:
                firstLiftUpTime_list.append(float(row[20]))  # first lift up timestamp
        files = getSortedSplitFile(path2, self.pid)
        for i in range(len(firstLiftUpTime_list)):
            self.readFile = path2 + files[i]
            self.loadLeapData()
            targetX_list.append(float(self.targetX))
            targetY_list.append(float(self.targetY))
            targetZ_list.append(float(self.targetZ))
            print firstLiftUpTime_list[i]
            loc = self.getFirstLiftUpCors(firstLiftUpTime_list[i])
            firstLiftUpX_list.append(float(self.frameArray[loc][offsetSplitX]))
            firstLiftUpY_list.append(float(self.frameArray[loc][offsetSplitY]))
            firstLiftUpZ_list.append(float(self.frameArray[loc][offsetSplitZ]))
            print 'targetX', 'targetY', 'targetZ', 'firstLiftUpX', 'firstLiftUpY', 'firstLiftUpZ'
            print self.targetX, self.targetY, self.targetZ, self.frameArray[loc][offsetSplitX], self.frameArray[loc][
                offsetSplitY], self.frameArray[loc][offsetSplitZ]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # draw the tablet plane
        X, Y, Z = self.drawTabletPlane()
        ax.scatter(X, Y, Z, c='c', alpha=0.1, marker='o', s=1)
        ax.scatter(targetX_list, targetY_list, targetZ_list, c='r', label='target', alpha=1, marker='o', s=90,
                   edgecolors='black')
        ax.scatter(firstLiftUpX_list, firstLiftUpY_list, firstLiftUpZ_list, c='c', label='First Lift Up', alpha=1,
                   marker='o', s=30, edgecolors='black')
        ax.set_xlabel('x(mm)')
        ax.set_ylabel('y(mm)')
        ax.set_zlabel('z(mm)')
        plt.title('Distribution of First Lift Up in 3D')
        plt.legend()
        plt.show()

    def drawRelativeTargetFirstLiftUpPlot3D(self, block, trial):
        fileandroid = path + "PId_" + str(self.pid) + "_TwoDFittsData_External.csv"
        offsetFirstLiftUp = 20
        # store 3D cors for target
        targetX_list = []
        targetY_list = []
        targetZ_list = []
        # the target is the center
        targetX_list.append(0)
        targetY_list.append(0)
        targetZ_list.append(0)
        # store 3D cors for first lift up
        firstLiftUpX_list = []
        firstLiftUpY_list = []
        firstLiftUpZ_list = []
        with open(fileandroid) as f:
            f_csv = csv.reader(f)
            for i in range(0, 10):  # skip the beginning
                next(f_csv)
            for row in f_csv:
                if str(row[offsetAndroidBlock]) == str(block) and str(row[offsetAndroidTrial]) == str(trial):
                    firstLiftUpTime = float(row[offsetFirstLiftUp])  # first lift up timestamp
                    break
        file = path2 + "PID_" + str(self.pid) + "_Block_" + str(block) + "_Trial_" + str(trial) + ".csv"
        self.readFile = file
        self.loadLeapData()
        loc = self.getFirstLiftUpCors(firstLiftUpTime)  # get the index of the first lift up frame
        firstLiftUpX_list.append(float(self.frameArray[loc][
                                           offsetSplitX]) - self.targetX)  # frameArray[loc] is the first Lift Up frame.Get the first List Up X cors.Then get the relative X
        firstLiftUpY_list.append(float(self.frameArray[loc][offsetSplitY]) - self.targetY)
        firstLiftUpZ_list.append(float(self.frameArray[loc][offsetSplitZ]) - self.targetZ)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(firstLiftUpX_list, firstLiftUpY_list, firstLiftUpZ_list, c='r', label='First Lift Up', alpha=1,
                   marker='o', s=30, edgecolors='black')
        ax.scatter(targetX_list, targetY_list, targetZ_list, c='c', label='target', alpha=1, marker='o', s=100,
                   edgecolors='black')
        margin = 40  # the margin of the plot
        ax.set_xlabel('x(mm)')
        ax.set_ylabel('y(mm)')
        ax.set_zlabel('z(mm)')
        ax.set_xlim(-1 * (margin), margin)
        ax.set_ylim(-1 * (margin), margin)
        ax.set_zlim(-1 * (margin), margin)
        plt.title('Distribution of First attempt relative to the target in single trial in 3D')
        plt.legend()
        plt.show()

    def drawRelativeTargetFirstLiftUpPlot2D(self, block, trial):
        file = path + "PId_" + str(self.pid) + "_TwoDFittsData_External.csv"
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
            for i in range(0, 10):  # skip the beginning
                next(f_csv)
            for row in f_csv:
                if int(row[2]) == block and int(row[3]) == trial:  # find the record with the block and trial
                    targetX = float(row[offsetTargetX]) * PixelToM  # change from pixel to mm
                    targetY = float(row[offsetTargetY]) * PixelToM
                    targetX_list.append(0)
                    targetY_list.append(0)
                    liftUpX = float(row[offsetLiftUpX]) * PixelToM
                    liftUpY = float(row[offsetLiftUpY]) * PixelToM
                    relaLiftUpX = liftUpX - targetX
                    relaLiftUpY = liftUpY - targetY
                    liftUpX_list.append(relaLiftUpX)
                    liftUpY_list.append(relaLiftUpY)
                    break
            # draw the picture
            plt.title('Distribution of First attempt relative to the target in single trial in 2D')
            plt.scatter(targetX_list, targetY_list, c='c', alpha=1, marker='o', label='target', s=100,
                        edgecolors='black')
            plt.scatter(liftUpX_list, liftUpY_list, c='r', alpha=1, marker='o', label='First_Lift_Up', s=30,
                        edgecolors='black')
            margin = 40  # the margin of the plot
            plt.xlim(-1 * (margin), margin)  # set the target point to be the center
            plt.ylim(-1 * (margin), margin)
            plt.xlabel('First Lift Up X(mm)')
            plt.ylabel('First Left Up Y(mm)')
            plt.legend()
            plt.grid(True)
            plt.show()

    # a helper function for drawing the tablet plane in a 3D plot
    # cumulate points to form a plane
    # return the point list of the plane
    def drawTabletPlane(self):
        X = []
        Y = []
        Z = []
        # use points to draw the tablet planee
        startX = -90
        startY = 0
        startZ = -48
        lengthX = 200
        # 45 * sqrt(2)
        lengthY = 60
        changeX = 0
        changeY = 0
        step = 0.8  # the density of the points in the plane
        while changeX < lengthX:
            changeY = 0
            while changeY < lengthY:
                X.append(startX + changeX)
                Y.append(startY + changeY)
                Z.append(
                    startZ - changeY)  # the angle is 45 degree, so the absolute change of Y and Z should be the same
                changeY += step
            changeX += step
        return X, Y, Z

    '''
    # this function is not used any more
    # draw the path of the finger
    def drawPath(self):
        files = getSortedSplitFile(path2, self.pid)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        colors = cm.rainbow(np.linspace(0, 1, len(files))) # different color represent different trial
        k=0 # iterator for the colors list
        for file in files:
            # store 3D cors for target
            startX_list = []
            startY_list = []
            startZ_list = []
            targetX_list = []
            targetY_list = []
            targetZ_list = []
            # store 3D cors for first lift up
            frameX_list = []
            frameY_list = []
            frameZ_list = []
            self.readFile = path2 + file
            keys = file.split('_')
            self.block = keys[3]
            self.trial = int(keys[5][0:-4])
            self.loadLeapData()
            targetX_list.append(self.targetX)
            targetY_list.append(self.targetY)
            targetZ_list.append(self.targetZ)
            startX_list.append(float(startThreeCor.x))
            startY_list.append(float(startThreeCor.y))
            startZ_list.append(float(startThreeCor.z))
            for frame in self.frameArray:
                frameX_list.append(float(frame[offsetSplitX]))
                frameY_list.append(float(frame[offsetSplitY]))
                frameZ_list.append(float(frame[offsetSplitZ]))

            ax.scatter(startX_list, startY_list, startZ_list, c='b', label='Start', alpha=1,
                       marker='+', s=100, edgecolors='black')
            ax.scatter(frameX_list, frameY_list, frameZ_list, c=colors[k], label='First Lift Up', alpha=1,
                       marker='o', s=30, edgecolors='black')
            ax.scatter(targetX_list, targetY_list, targetZ_list, c='c', label='target', alpha=1, marker='o', s=100,
                       edgecolors='black')
            k=k+1

        # draw the tablet plane
        X, Y, Z = self.drawTabletPlane()
        ax.scatter(X, Y, Z, c='c', alpha=0.1, marker='o', s=1)
        ax.set_xlabel('x(mm)')
        ax.set_ylabel('y(mm)')
        ax.set_zlabel('z(mm)')
        plt.title('path of fingers in an experiment')
        plt.legend()
        plt.show()
    '''

    # draw the path of the finger
    def drawStartAndEnd(self,mode):
        files = getSortedSplitFile(path2, self.pid)
        # the key is the direction
        # the value is a list of value in the class of FingerPath
        FingerPath_map = {}
        for file in files:
            self.readFile = path2 + file
            keys = file.split('_')
            self.block = keys[3]
            self.trial = int(keys[5][0:-4])
            self.loadLeapData()
            # if the current direction does not exist in the map
            # create new position list for the current direction
            if not FingerPath_map.has_key(self.direction):
               FingerPath_map[self.direction]=[]
            # else just append in the original list
            # the start point of the path
            StartPathX = []
            StartPathY = []
            StartPathZ = []
            # the end point of the path
            EndPathX = []
            EndPathY = []
            EndPathZ = []
            # the points in the  intermediate path
            InterPathX = []
            InterPathY = []
            InterPathZ = []

            # store the location of the start of the path
            StartPathX.append(self.startPathThreeCor.x+offset3DX)
            StartPathY.append(self.startPathThreeCor.y+offset3DY)
            StartPathZ.append(self.startPathThreeCor.z+offset3DZ)
            # store the location of the end of the path
            EndPathX.append(self.endPathThreeCor.x+offset3DX)
            EndPathY.append(self.endPathThreeCor.y+offset3DY)
            EndPathZ.append(self.endPathThreeCor.z+offset3DZ)
            # store the path of the finger excluding the start and end

            for i in range(1,self.numberFrame-1):
                InterPathX.append(float(self.frameArray[i][offsetSplitX])+offset3DX)
                InterPathY.append(float(self.frameArray[i][offsetSplitY])+offset3DY)
                InterPathZ.append(float(self.frameArray[i][offsetSplitZ])+offset3DZ)

            fingerPath = FingerPath(StartPathX,StartPathY,StartPathZ,EndPathX,EndPathY,EndPathZ,InterPathX,InterPathY,InterPathZ)
            FingerPath_map[self.direction].append(fingerPath)

        maxPath=30
        colors = cm.rainbow(np.linspace(0, 1, maxPath))

        for key in FingerPath_map.keys():
            # with accurate start coordinate in 3D,calculate the target 3D
            # key is the current direction
            targetThreeCor = getTargetLocationFor3DWithDirection(key,self.amplitude)

            # used for draw the real start button and real target
            # the draw plot function need list for x,y,z as input

            RealStartX_list=[]
            RealStartY_list=[]
            RealStartZ_list=[]
            RealTargetX_list=[]
            RealTargetY_list=[]
            RealTargetZ_list=[]

            RealStartX_list.append(startThreeCor.x)
            RealStartY_list.append(startThreeCor.y)
            RealStartZ_list.append(startThreeCor.z)

            RealTargetX_list.append(targetThreeCor.x)
            RealTargetY_list.append(targetThreeCor.y)
            RealTargetZ_list.append(targetThreeCor.z)

            fig = plt.figure()
            if mode==3:
                ax = fig.add_subplot(111, projection='3d')
                if key == 90.0 or key == 270.0:
                    ax.view_init(30, 35)

            k=0
            for p in FingerPath_map[key]:
                if k==maxPath:
                    break
                if mode==3:
                    ax.scatter(p.StartPathX, p.StartPathY,p.StartPathZ, c=colors[k], label = 'Start', alpha = 1,marker = '+', s = 30, edgecolors = 'black')
                    ax.scatter(p.EndPathX,p.EndPathY,p.EndPathZ, c=colors[k], label='First Lift Up', alpha=1,marker='o', s=30, edgecolors='black')
                    #ax.scatter(p.InterPathX, p.InterPathY,p.InterPathZ, c=colors[k], label = 'Start', alpha = 1,marker = 'o', s = 30)
                else:
                    plt.scatter(p.StartPathX, p.StartPathY, c=colors[k], label='Start', alpha=1,marker='+', s=30, edgecolors='black')
                    plt.scatter(p.EndPathX, p.EndPathY, c=colors[k], label='First Lift Up', alpha=1,marker='o', s=30, edgecolors='black')
                    #plt.scatter(p.InterPathX, p.InterPathY, c=colors[k], label='Start', alpha=1,marker='o', s=30)
                k=k+1

            if mode==3:
                ax.scatter(RealStartX_list, RealStartY_list, RealStartZ_list, c='r', label='Real start', alpha=1,
                       marker='o', s=200)
                ax.scatter(RealTargetX_list, RealTargetY_list,RealTargetZ_list, c='y', label='First Lift Up', alpha=1,
                       marker='o', s=200)
            else:
                plt.scatter(RealStartX_list, RealStartY_list, c='r', label='Real start', alpha=1,
                           marker='o', s=200)
                plt.scatter(RealTargetX_list, RealTargetY_list, c='y', label='First Lift Up', alpha=1,
                           marker='o', s=200)

            if mode==3:
                ax.set_zlabel('Z(mm)')
                ax.set_ylabel('Y(mm)')
                ax.set_xlabel('X(mm)')
            else:
                plt.xlabel('X(mm)')
                plt.ylabel('Y(mm)')

            plt.title('start and end points of path in an experiment with direction of '+str(key))
            if mode==2:
                plt.grid()
            plt.show()









# test function
def test_DrawPlots():
    pid=851
    drawPlots=DrawPlots(pid)
    #drawPlots.drawPath()
    mode=2
    drawPlots.drawStartAndEnd(mode)

test_DrawPlots()
