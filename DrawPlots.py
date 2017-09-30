# this function is used to draw plots

import matplotlib.cm as cm
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
import  matplotlib
from GlobalVariables import *
from mpl_toolkits.mplot3d import Axes3D

# import helper functions from other script
from GlobalVariables import startThreeCor
from GlobalVariables import  offset3DX
from GlobalVariables import  offset3DY
from GlobalVariables import offset3DZ

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

from GlobalVariables import offsetSplitWidth
from GlobalVariables import ThreeCorPoint

from FileUtils import getSortedSplitFile

from SpaceUtils import getTargetLocationFor3DWithDirection
from SpaceUtils import  getTargetLocationFor3D
from SpaceUtils import LocationInProjectedPlane



# used as keys in finger_maps
class Combination:

    direction=0
    width=0
    amplitude=0

    def __init__(self,direction,width,amplitude):
        self.direction=direction
        self.width=width
        self.amplitude=amplitude

    def __eq__(self, other):
        return self.direction==other.direction and self.width==other.width and self.amplitude==other.amplitude

    def __hash__(self):
        return hash(str(self.direction) + str(self.width)+str(self.amplitude))

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
    frameArray = []
    numberFrame = 0
    combination=Combination(0,0,0)
    projectedStartPathThreeCor=0
    projectedEndPathThreeCor=0
    sizeOfStartCircle=300
    readFile=""

    targetX = 0
    targetY = 0
    targetZ = 0




    path="" # the path for the raw file

    path2=""
    def __init__(self,pid,path):

        self.pid=pid
        self.frameArray = []
        self.numberFrame = 0
        self.path=path
        self.path2=self.path+'split/'


    def loadLeapData(self):

        self.frameArray = []

        with open(self.readFile) as f:
            f_csv = csv.reader(f)
            next(f_csv)  # skip the header
            for row in f_csv:
                self.frameArray.append(row)

        self.numberFrame = len(self.frameArray)

        direction = float(self.frameArray[0][offsetSplitDirection])
        width = float(self.frameArray[0][offsetSplitWidth])
        amplitude=float(self.frameArray[0][offsetSplitAmplitude])
        self.combination=Combination(direction,width,amplitude)

        targetThreeCor = getTargetLocationFor3D(self.pid, self.block,self.trial,self.path)  # with accurate start coordinate in 3D,calculate the target 3D

        self.targetX = targetThreeCor.x
        self.targetY = targetThreeCor.y
        self.targetZ = targetThreeCor.z








    # go through all the trials in one experiment
    # draw targets and each first lift up points
    # the target is represented with green color
    # where the lift up points are represented with red color
    def drawTargetFirstLiftUpPlot2D(self,pathForPlot):

        file = self.path + "PId_" + str(self.pid) + "_TwoDFittsData_External.csv"

        with open(file) as f:

            targetX_list = []
            targetY_list = []
            liftUpX_list = []
            liftUpY_list = []
            f_csv = csv.reader(f)
            for i in range(0, 10):  # skip the beginning
                next(f_csv)
             # draw the picture
            plotTitle = 'Distribution of First Lift Up in 2D in one trial'
            # we need to make the scale of x and y equal
            plt.figure(figsize=(5, 5), dpi=100)
            plt.title(plotTitle)

            width=0

            for row in f_csv:

                targetX_list=[]
                targetY_list=[]

                if width == 0:
                    width = float(row[offsetAndroidWidth])
                    #print width
                    sizeOfTarget = 0
                    if abs(width - 4.88) < 0.5:
                        sizeOfTarget = 180
                    if abs(width - 7.22) < 0.5:
                        sizeOfTarget = 340
                    if abs(width - 9.22) < 0.5:
                        sizeOfTarget = 500
                    width=0
                targetX_list.append(float(row[offsetAndroidTargetX]) * PixelToM)  # change from Pixel to mm
                targetY_list.append(float(row[offsetAndroidTargetY]) * PixelToM)
                liftUpX_list.append(float(row[offsetAndroidFirstLiftUpX]) * PixelToM)
                liftUpY_list.append(float(row[offsetAndroidFirstLiftUpY]) * PixelToM)
                plt.scatter(targetX_list, targetY_list, c='c', alpha=1, marker='o', s=sizeOfTarget,
                            edgecolors='black')


            matplotlib.rcParams.update({'font.size': 10})

            plt.scatter(liftUpX_list, liftUpY_list, c='r', alpha=1, marker='o', s=30,
                        edgecolors='black')

            plt.xlabel('First Lift Up X(mm)')
            plt.ylabel('First Left Up Y(mm)')
            plt.legend()
            plt.grid(True)
            plt.savefig(pathForPlot + plotTitle + '.png')
            #plt.show()

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
    def drawTargetFirstLiftUpPlot3D(self,pathForPlot):
        fileandroid = self.path + "PId_" + str(self.pid) + "_TwoDFittsData_External.csv"
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

                width = float(row[offsetAndroidWidth])
                sizeOfTarget = 0
                if abs(width - 4.88) < 0.5:
                    sizeOfTarget = 120
                if abs(width - 7.22) < 0.5:
                    sizeOfTarget = 320
                if abs(width - 9.22) < 0.5:
                    sizeOfTarget = 600

                firstLiftUpTime_list.append(float(row[20]))  # first lift up timestamp

        files = getSortedSplitFile(self.path2, self.pid)
        for i in range(len(firstLiftUpTime_list)):
            self.readFile = self.path2 + files[i]
            filenameSplit=files[i].split('_')
            self.block = int(filenameSplit[3])
            self.trial = int(filenameSplit[5][0:-4])
            self.loadLeapData()
            targetX_list.append(float(self.targetX))
            targetY_list.append(float(self.targetY))
            targetZ_list.append(float(self.targetZ))
            #print firstLiftUpTime_list[i]
            loc = self.getFirstLiftUpCors(firstLiftUpTime_list[i])
            firstLiftUpX_list.append(float(self.frameArray[loc][offsetSplitX]))
            firstLiftUpY_list.append(float(self.frameArray[loc][offsetSplitY]))
            firstLiftUpZ_list.append(float(self.frameArray[loc][offsetSplitZ]))
            #print 'targetX', 'targetY', 'targetZ', 'firstLiftUpX', 'firstLiftUpY', 'firstLiftUpZ'
            #print self.targetX, self.targetY, self.targetZ, self.frameArray[loc][offsetSplitX], self.frameArray[loc][offsetSplitY], self.frameArray[loc][offsetSplitZ]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        #ax=self.create3DPlots()
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
        matplotlib.rcParams.update({'font.size': 10})
        plotTitle='Distribution of First Lift Up in 3D in one trial'
        plt.title(plotTitle)
        plt.legend()
        plt.savefig(pathForPlot + plotTitle + '.png')
        #plt.show()

    def drawRelativeTargetFirstLiftUpPlot3D(self,pathForPlot):

        # get the index of firstLiftUp in android files
        fileandroid = self.path + "PId_" + str(self.pid) + "_TwoDFittsData_External.csv"
        offsetFirstLiftUp = 20

        firstLiftUpTimeList=[] # store the timestamp for all the first lift up of frames in a trial

        with open(fileandroid) as f:

            f_csv = csv.reader(f)

            for i in range(0, 10):  # skip the beginning
                next(f_csv)

            for row in f_csv:
                firstLiftUpTimeList.append(float(row[offsetFirstLiftUp]))  # first lift up timestamp


        files = getSortedSplitFile(self.path2, self.pid)



        for file in files:
            keys = file.split('_')
            block = keys[3]
            trial = int(keys[5][0:-4])

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


            file = self.path+'split/' + "PID_" + str(self.pid) + "_Block_" + str(block) + "_Trial_" + str(trial) + ".csv"
            self.readFile = file
            self.block = block
            self.trial = trial
            self.loadLeapData()
            width = float(self.frameArray[0][offsetSplitWidth])


            sizeOfTarget = 0
            if abs(width - 4.88) < 0.5:
                sizeOfTarget = 250
            if abs(width - 7.22) < 0.5:
                sizeOfTarget = 600
            if abs(width - 9.22) < 0.5:
                sizeOfTarget = 1000

            index = self.getFirstLiftUpCors(firstLiftUpTimeList[i])  # get the index of the first lift up frame

            firstLiftUpX_list.append(float(self.frameArray[index][
                                               offsetSplitX]) - self.targetX)  # frameArray[loc] is the first Lift Up frame.Get the first List Up X cors.Then get the relative X
            firstLiftUpY_list.append(float(self.frameArray[index][offsetSplitY]) - self.targetY)
            firstLiftUpZ_list.append(float(self.frameArray[index][offsetSplitZ]) - self.targetZ)

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(firstLiftUpX_list, firstLiftUpY_list, firstLiftUpZ_list, c='r', label='First Lift Up', alpha=1,
                       marker='o', s=30, edgecolors='black')
            ax.scatter(targetX_list, targetY_list, targetZ_list, c='c', label='target', alpha=1, marker='o', s=sizeOfTarget,
                       edgecolors='black')

            margin = 40  # the margin of the plot
            ax.set_xlabel('x(mm)')
            ax.set_ylabel('y(mm)')
            ax.set_zlabel('z(mm)')
            ax.set_xlim(-1 * (margin), margin)
            ax.set_ylim(-1 * (margin), margin)
            ax.set_zlim(-1 * (margin), margin)
            matplotlib.rcParams.update({'font.size': 10})
            plotTitle = 'Distribution Of Relative First attempt in 3D with block_' + str(block) + ' trial_' + str(trial)
            plt.title(plotTitle)
            plt.legend()
            plt.savefig(pathForPlot + 'relative_3d' +'/'+ plotTitle + '.png')
            #plt.show()


    def drawRelativeTargetFirstLiftUpPlot2D(self,pathForPlot):
        file = self.path + "PId_" + str(self.pid) + "_TwoDFittsData_External.csv"

        offsetTargetX = 12
        offsetTargetY = 13
        offsetLiftUpX = 16
        offsetLiftUpY = 17

        with open(file) as f:
            f_csv = csv.reader(f)
            for i in range(0, 10):  # skip the beginning
                next(f_csv)

            for row in f_csv:

                width = float(row[offsetAndroidWidth])

                sizeOfTarget = 0
                if abs(width - 4.88) < 0.5:
                    sizeOfTarget = 250
                if abs(width - 7.22) < 0.5:
                    sizeOfTarget = 600
                if abs(width - 9.22) < 0.5:
                    sizeOfTarget = 1000

                targetX_list = []
                targetY_list = []
                liftUpX_list = []
                liftUpY_list = []
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
                matplotlib.rcParams.update({'font.size': 10})
                plt.figure(figsize=(5, 5), dpi=100)
                # draw the picture
                plotTitle = 'Distribution Of Relative First attempt in 2D with block_' + str(
                    row[offsetAndroidBlock]) + ' trial_' + str(row[offsetAndroidTrial])
                plt.title(plotTitle)
                plt.scatter(targetX_list, targetY_list, c='c', alpha=1, marker='o',  s=sizeOfTarget,
                            )
                plt.scatter(liftUpX_list, liftUpY_list, c='r', alpha=1, marker='o',  s=30,
                            )
                margin = 40  # the margin of the plot
                plt.xlim(-1 * (margin), margin)  # set the target point to be the center
                plt.ylim(-1 * (margin), margin)
                plt.xlabel('First Lift Up X(mm)')
                plt.ylabel('First Lift Up Y(mm)')
                plt.legend()
                plt.grid(True)
                plt.savefig(pathForPlot + 'relative_2d' +'/'+ plotTitle + '.png')
                #plt.show()


    # a helper function for drawing the tablet plane in a 3D plot
    # cumulate points to form a plane
    # return the point list of the plane
    def drawTabletPlane(self):

        X = []
        Y = []
        Z = []

        lengthX = 200 # half the length
        lengthY = 40 # half the width
        changeX = 0
        step = 2  # the density of the points in the plane
        while changeX < lengthX:
            changeY = 0
            while changeY < lengthY:
                X.append(start3DX + changeX)
                Y.append(start3DY + changeY)
                Z.append(start3DZ - changeY)  # the angle is 45 degree, so the absolute change of Y and Z should be the same
                changeY += step
            changeX += step
        changeX=0
        while changeX < lengthX:
            changeY = 0
            while changeY < lengthY:
                X.append(start3DX - changeX)
                Y.append(start3DY - changeY)
                Z.append(start3DZ + changeY)  # the angle is 45 degree, so the absolute change of Y and Z should be the same
                changeY += step
            changeX += step
        changeX = 0
        while changeX < lengthX:
            changeY = 0
            while changeY < lengthY:
                X.append(start3DX + changeX)
                Y.append(start3DY - changeY)
                Z.append(start3DZ + changeY)  # the angle is 45 degree, so the absolute change of Y and Z should be the same
                changeY += step
            changeX += step
        changeX = 0
        while changeX < lengthX:
            changeY = 0
            while changeY < lengthY:
                X.append(start3DX - changeX)
                Y.append(start3DY + changeY)
                Z.append(start3DZ - changeY)  # the angle is 45 degree, so the absolute change of Y and Z should be the same
                changeY += step
            changeX += step
        return X, Y, Z



    # this function is used to store the data of fingers in a map
    def setUpForFingerPath_map(self):

        files = getSortedSplitFile(self.path2, self.pid)

        # the key is the direction
        # the value is a list of value in the class of FingerPath
        fingerPath_map = {}

        for file in files:

            self.readFile = self.path2 + file
            keys = file.split('_')
            self.block = keys[3]
            self.trial = int(keys[5][0:-4])
            self.loadLeapData() # set the  combination(width,amplitude,direction) for the drawPlots class
            # if the current direction does not exist in the map
            # create new position list for the current direction
            if not fingerPath_map.has_key(self.combination):
                fingerPath_map[self.combination] = []

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

            # the start of the path is the first frame
            # construct a three-cor class with x,y and z
            # offset3DX,offset3DY,offset3DZ mean the offset between the position measured by leap motion and the real location measured by ruler
            startPathThreeCor = ThreeCorPoint(float(self.frameArray[0][offsetSplitX]) + offset3DX,
                                              float(self.frameArray[0][offsetSplitY]) + offset3DY,
                                              float(self.frameArray[0][offsetSplitZ]) + offset3DZ)

            self.projectedStartPathThreeCor = LocationInProjectedPlane(
                startPathThreeCor)  # project it in a system that tablet is vertical to the ground

            endPathThreeCor = ThreeCorPoint(float(self.frameArray[self.numberFrame - 1][offsetSplitX]) + offset3DX,
                                            float(self.frameArray[self.numberFrame - 1][offsetSplitY]) + offset3DY,
                                            float(self.frameArray[self.numberFrame - 1][offsetSplitZ]) + offset3DZ)

            self.projectedEndPathThreeCor = LocationInProjectedPlane(endPathThreeCor)  # project it in a system that tablet is vertical to the ground

            # store the location of the start of the path
            StartPathX.append(self.projectedStartPathThreeCor.x)
            StartPathY.append(self.projectedStartPathThreeCor.y)
            StartPathZ.append(self.projectedStartPathThreeCor.z)
            # store the location of the end of the path
            EndPathX.append(self.projectedEndPathThreeCor.x)
            EndPathY.append(self.projectedEndPathThreeCor.y)
            EndPathZ.append(self.projectedEndPathThreeCor.z)
            # store the path of the finger excluding the start and end

            for i in range(1, self.numberFrame - 1):
                # construct a 3D point class for the path point
                pathThreeCor = ThreeCorPoint(float(self.frameArray[i][offsetSplitX]) + offset3DX,
                                             float(self.frameArray[i][offsetSplitY]) + offset3DY,
                                             float(self.frameArray[i][offsetSplitZ]) + offset3DZ)
                # project it in the system that tablet is vertical to the ground
                projectedPathThreeCor = LocationInProjectedPlane(pathThreeCor)
                InterPathX.append(projectedPathThreeCor.x)
                InterPathY.append(projectedPathThreeCor.y)
                InterPathZ.append(projectedPathThreeCor.z)
            fingerPath = FingerPath(StartPathX, StartPathY, StartPathZ, EndPathX, EndPathY, EndPathZ, InterPathX,
                                    InterPathY, InterPathZ)

            fingerPath_map[self.combination].append(fingerPath)

        return fingerPath_map


    def setUpRealStartAndTargetList(self,key):

        # with accurate start coordinate in 3D,calculate the target 3D
        # key is the current direction
        # we do not need to add offset3DX,offset3DY,offset3DZ to startThreeCor since it's the real position measured by ruler
        # project it to a system that tablet is vertical to the ground
        projectedStartThreeCor = LocationInProjectedPlane(startThreeCor)
        # since targetThreeCor is calculated based on the startThreeCor,amplitude and direction,it also do not need to add offset3DX,offset3DY,offset3DZ
        targetThreeCor = getTargetLocationFor3DWithDirection(key.direction, key.amplitude)
        # project it to a system that tablet is vertical to the ground
        projectedTargetThreeCor = LocationInProjectedPlane(targetThreeCor)

        # used for draw the real start button and real target
        # the draw plot function need list for x,y,z as input

        RealStartX_list = []
        RealStartY_list = []
        RealStartZ_list = []

        RealTargetX_list = []
        RealTargetY_list = []
        RealTargetZ_list = []

        RealStartX_list.append(projectedStartThreeCor.x)
        RealStartY_list.append(projectedStartThreeCor.y)
        RealStartZ_list.append(projectedStartThreeCor.z)

        RealTargetX_list.append(projectedTargetThreeCor.x)
        RealTargetY_list.append(projectedTargetThreeCor.y)
        RealTargetZ_list.append(projectedTargetThreeCor.z)

        return RealStartX_list,RealStartY_list,RealStartZ_list,RealTargetX_list,RealTargetY_list,RealTargetZ_list

    # draw the path of the finger
    def drawStartAndEnd(self,pathForPlot):


        fingerPath_map=self.setUpForFingerPath_map()

        dimensionList = [2, 3]  # 2d/3d
        modeList = ['start_and_end', 'path']  # 1 represent start and end,2 represent path

        for dimension in dimensionList:

            for mode in modeList:

                for key in fingerPath_map.keys():

                    # get the list for drawing real start,real target and real target
                    RealStartX_list, RealStartY_list, RealStartZ_list, RealTargetX_list, RealTargetY_list, RealTargetZ_list=self.setUpRealStartAndTargetList(key)

                    fig = plt.figure()

                    # the range of x
                    minX = -60
                    maxX = 60
                    # the range of y
                    minY = 20
                    maxY = 140

                    # the size for drawing target cricle
                    sizeOfTargetCircle = 0

                    # calculate the size of the target
                    if abs(key.width - 4.88) < 0.5:
                        sizeOfTargetCircle = 120
                    if abs(key.width - 7.22) < 0.5:
                        sizeOfTargetCircle = 310
                    if abs(key.width - 9.22) < 0.5:
                        sizeOfTargetCircle = 500

                    '''
                    # how many paths of trials will be shown in the plot
                    if mode == 'start_and_end':
                        maxNumOfPath = 30
                    else:
                        maxNumOfPath = 4  # too much path will make the whole plot a mass
                    '''

                    colors = cm.rainbow(np.linspace(0, 1, 10))  # color list for different trial in one plot

                    if dimension == 3:

                        ax = fig.add_subplot(111, projection='3d')
                        ax.set_aspect('equal')  # to ensure x,y and z have then same scale


                    else:  # 2D
                        # we need to make the scale of x and y equal
                        plt.figure(figsize=(5, 5), dpi=100)
                        plt.xlim(minX, maxX)
                        plt.ylim(minY, maxY)

                    # draw the real start and target
                    if dimension == 3:

                        # draw the center of the start circle
                        ax.scatter(RealStartX_list, RealStartY_list, RealStartZ_list, c='b', label='Real start',
                                   alpha=1, marker='o', s=1)
                        # draw the start button at real size
                        ax.scatter(RealStartX_list, RealStartY_list, RealStartZ_list, c='r', label='Real start',
                                   alpha=1, marker='o', s=self.sizeOfStartCircle)
                        # in case the center is covered by the circle, we draw it again
                        # draw the center of the start circle
                        ax.scatter(RealStartX_list, RealStartY_list, RealStartZ_list, c='b', label='Real start',
                                   alpha=1, marker='o', s=1)
                        # draw the center of the target circle
                        ax.scatter(RealTargetX_list, RealTargetY_list, RealTargetZ_list, c='b', label='First Lift Up',
                                   alpha=1, marker='o', s=1)
                        # draw the target button at real size
                        ax.scatter(RealTargetX_list, RealTargetY_list, RealTargetZ_list, c='y', label='First Lift Up',
                                   alpha=1, marker='o', s=sizeOfTargetCircle)

                    else:

                        # draw the start button at real size
                        plt.scatter(RealStartX_list, RealStartY_list, c='r', label='Real start', alpha=1, marker='o',
                                    s=self.sizeOfStartCircle)
                        # draw the center of the start circle
                        plt.scatter(RealStartX_list, RealStartY_list, c='b', label='Real start', alpha=1, marker='o',
                                    s=1)
                        # draw the target at real size
                        plt.scatter(RealTargetX_list, RealTargetY_list, c='y', label='First Lift Up', alpha=1,
                                    marker='o', s=sizeOfTargetCircle)
                        # draw the target center
                        plt.scatter(RealTargetX_list, RealTargetY_list, c='b', label='First Lift Up', alpha=1,
                                    marker='o', s=1)


                    # draw the path or start and end
                    k = 0
                    for p in fingerPath_map[key]: # all the trials with the same combination of width,direction and amplitude

                        #if k == maxNumOfPath:
                            #break

                        if dimension == 3:

                            ax.scatter(p.StartPathX, p.StartPathY, p.StartPathZ, c=colors[k], label='Start', alpha=1,
                                       marker='+', s=10, edgecolors='black')
                            ax.scatter(p.EndPathX, p.EndPathY, p.EndPathZ, c=colors[k], label='First Lift Up', alpha=1,
                                       marker='o', s=10, edgecolors='black')

                            if mode == 'path':
                                ax.scatter(p.InterPathX, p.InterPathY, p.InterPathZ, c=colors[k], label='Start',
                                           alpha=1, marker='o', s=10)
                        else:

                            plt.scatter(p.StartPathX, p.StartPathY, c=colors[k], alpha=1, marker='+', s=10)
                            plt.scatter(p.EndPathX, p.EndPathY, c=colors[k], alpha=1, marker='o', s=10)

                            if mode == 'path':
                                plt.scatter(p.InterPathX, p.InterPathY, c=colors[k], alpha=1, marker='o', s=10)

                        k = k + 1

                    if dimension == 3:

                        ax.set_zlabel('Z(mm)')
                        ax.set_ylabel('Y(mm)')
                        ax.set_xlabel('X(mm)')
                        self.set_axes_equal(ax)



                    else:
                        plt.xlabel('X(mm)')
                        plt.ylabel('Y(mm)')

                    matplotlib.rcParams.update({'font.size': 10})
                    plotTitle=str(dimension)+'d_'+'direction_' + str(round(key.direction, 0)) + '_width_' + str(round(key.width, 2)) + '_amplitude_' + str(round(key.amplitude, 2))
                    plt.title(plotTitle)

                    if dimension == 2:
                        plt.grid()

                    fig.set_size_inches(6, 6)
                    plt.savefig(pathForPlot+ str(dimension) + 'd_' + 'mode_' + str(mode)+'/'+plotTitle+'.png')


    # draw the distribution of pause


    # this function is used for helping make the scale of x,y and z the same
    def set_axes_equal(self, ax):

        """Fix equal aspect bug for 3D plots."""

        xlim = ax.get_xlim3d()
        ylim = ax.get_ylim3d()
        zlim = ax.get_zlim3d()

        from numpy import mean
        xmean = mean(xlim)-3
        ymean = mean(ylim)
        zmean = mean(zlim)

        plot_radius = max([abs(lim - mean_)
                           for lims, mean_ in ((xlim, xmean),
                                               (ylim, ymean),
                                               (zlim, zmean))
                           for lim in lims])

        ax.set_xlim3d([xmean - plot_radius, xmean + plot_radius])
        ax.set_ylim3d([ymean - plot_radius, ymean + plot_radius])
        ax.set_zlim3d([zmean - plot_radius, zmean + plot_radius])







