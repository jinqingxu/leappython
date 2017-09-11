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

# import helper functions from other script

from GlobalVariables import path2
from GlobalVariables import offsetSplitX
from GlobalVariables import  offsetSplitY
from GlobalVariables import offsetSplitZ
from GlobalVariables import  offsetSplitTimestamp
from GlobalVariables import offsetSplitDirection
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
from SpaceUtils import getTargetLocationFor3D
from GlobalVariables import ThreeCorPoint

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
        self.direction=self.frameArray[0][offsetSplitDirection]
        # the start of the path is the first frame
        # construct a three-cor class with x,y and z
        self.startPathThreeCor=ThreeCorPoint(float(self.frameArray[0][offsetSplitX]),float(self.frameArray[0][offsetSplitY]),float(self.frameArray[0][offsetSplitZ]))
        self.endPathThreeCor=ThreeCorPoint(float(self.frameArray[self.numberFrame-1][offsetSplitX]),float(self.frameArray[self.numberFrame-1][offsetSplitY]),float(self.frameArray[self.numberFrame-1][offsetSplitZ]))


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

    # draw the path of the finger
    def drawStartAndEnd(self,numOfDirection):
        files = getSortedSplitFile(path2, self.pid)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        colors = cm.rainbow(np.linspace(0, 1, numOfDirection))  # different color represent different trial
        # the key is the direction
        # the value is a list of start point of each trial
        startPoint_map = {}
        # the key is the direction
        # the value is a list of end point of each trial
        endPoint_map= {}
        for file in files:
            self.readFile = path2 + file
            keys = file.split('_')
            self.block = keys[3]
            self.trial = int(keys[5][0:-4])
            self.loadLeapData()
            # if the current direction does not exist in the map
            # create new position list for the current direction
            if not startPoint_map.has_key(self.direction):
                startPoint_map[self.direction]=[]
                endPoint_map[self.direction]=[]
            # else just append in the original list
            startPoint_map[self.direction].append(self.startPathThreeCor)
            endPoint_map[self.direction].append(self.endPathThreeCor)
        k=0
        for key in startPoint_map.keys():
            # construct the x,y,z list for drawing plots
            startX_list=[] # the x value of a start point
            startY_list=[] # the y value of a start point
            startZ_list=[] # the z value of a start point
            endX_list=[] # the x value of an end point
            endY_list=[] # the y value of an end point
            endZ_list=[] # the z value of an end point
            # go through the start point list for the current direction
            for p in startPoint_map[key]:
                startX_list.append(p.x)
                startY_list.append(p.y)
                startZ_list.append(p.z)
            for p in endPoint_map[key]:
                endX_list.append(p.x)
                endY_list.append(p.y)
                endZ_list.append(p.z)
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            ax.scatter(startX_list, startY_list, startZ_list, c='b', label = 'Start', alpha = 1,
                                                                                     marker = '+', s = 30, edgecolors = 'black')
            ax.scatter(endX_list, endY_list, endZ_list, c=colors[k], label='First Lift Up', alpha=1,
                       marker='o', s=30, edgecolors='black')
            ax.set_xlabel('x(mm)')
            ax.set_ylabel('y(mm)')
            ax.set_zlabel('z(mm)')
            plt.title('start and end points of path in an experiment with direction of '+str(key))
            plt.legend()
            plt.show()

            k=k+1

        # draw the tablet plane
        '''
        X, Y, Z = self.drawTabletPlane()
        ax.scatter(X, Y, Z, c='c', alpha=0.1, marker='o', s=1)
        '''







# test function
def test_DrawPlots():
    pid=851
    numOfDirection=4
    drawPlots=DrawPlots(pid)
    #drawPlots.drawPath()
    drawPlots.drawStartAndEnd(numOfDirection)

test_DrawPlots()
