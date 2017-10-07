# this function is used to draw plots

import matplotlib.cm as cm
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
import  matplotlib

from mpl_toolkits.mplot3d import Axes3D

# import helper functions from other script

from GlobalVariables import *

from FileUtils import getSortedSplitFile
from SpaceUtils import  *



class TargetForPlot2D:
    x=0
    y=0
    size=0

    def __init__(self,x,y,size):
        self.x=x
        self.y=y
        self.size=size

    def __eq__(self,other):
        return self.x==other.x and self.y==other.y and self.size==other.size

class TargetForPlot3D:
    x = 0
    y = 0
    z = 0
    size = 0

    def __init__(self, x, y, z, size):
        self.x = x
        self.y = y
        self.z = z
        self.size = size

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z==other.z and self.size == other.size

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

    targetWidth=0

    offset3DX=0
    offset3DY=0
    offset3DZ=0

    path="" # the path for the raw file

    path2=""

    def loadLeapData(self):

        self.frameArray = []

        with open(self.readFile) as f:
            f_csv = csv.reader(f)
            next(f_csv)  # skip the header
            for row in f_csv:
                self.frameArray.append(row)

        self.numberFrame = len(self.frameArray)

        direction = float(self.frameArray[0][colNumSplitDirection])
        width = float(self.frameArray[0][colNumSplitWidth])
        amplitude=float(self.frameArray[0][colNumSplitAmplitude])
        self.combination=Combination(direction,width,amplitude)

        targetThreeCor = getTargetLocationFor3D(self.pid, self.block,self.trial,self.path)  # with accurate start coordinate in 3D,calculate the target 3D

        self.targetX = targetThreeCor.x
        self.targetY = targetThreeCor.y
        self.targetZ = targetThreeCor.z

        self.targetWidth=float(self.frameArray[0][colNumSplitWidth])

        self.offset3DX,self.offset3DY,self.offset3DZ=getOffetXYZ(self.pid)

    def drawAllTargetFirstLiftUpPlot2D(self,path):

        fileForAllParticipants=path+'All_First_Lift_Up_2D.csv'
        firstLiftUpXForOlds=[]
        firstLiftUpYForOlds=[]
        firstLiftUpXForYoungs=[]
        firstLiftUpYForYoungs=[]
        firstRelaLiftUpXForOlds=[]
        firstRelaLiftUpYForOlds=[]
        firstRelaLiftUpXForYoungs=[]
        firstRelaLiftUpYForYoungs=[]
        colNumFirstLiftUpX=1
        colNumFirstLiftUpY=2
        colNumRelaFirstLiftUpX=3
        colNumRelaFirstLiftUpY=4
        # load all the liftUp and relative liftUp data
        with open(fileForAllParticipants) as f:
            f_csv = csv.reader(f)
            next(f_csv)
            for row in f_csv:
                if float(row[0])<200:
                    firstLiftUpXForOlds.append(float(row[colNumFirstLiftUpX]))
                    firstLiftUpYForOlds.append(float(row[colNumFirstLiftUpY]))
                    firstRelaLiftUpXForOlds.append(float(row[colNumRelaFirstLiftUpX]))
                    firstRelaLiftUpYForOlds.append(float(row[colNumRelaFirstLiftUpY]))

                else:
                    firstLiftUpXForYoungs.append(float(row[colNumFirstLiftUpX]))
                    firstLiftUpYForYoungs.append(float(row[colNumFirstLiftUpY]))
                    firstRelaLiftUpXForYoungs.append(float(row[colNumRelaFirstLiftUpX]))
                    firstRelaLiftUpYForYoungs.append(float(row[colNumRelaFirstLiftUpY]))
        # load all the target data
        fileForAllTargets=path+'All_Target_2D.csv'

        with open(fileForAllTargets) as f:

            f_csv=csv.reader(f)
            next(f_csv)
            targetForPlot_list=[]
            for row in f_csv:
                targetForPlot_list.append(TargetForPlot2D(float(row[0]),float(row[1]),float(row[2])))
        plotTitle='Distribution of first lift up for all old adults'
        self.helpDrawTargetFirstLiftUpPlot2D(plotTitle,pathHeaderForAllOldAdults,targetForPlot_list,firstLiftUpXForOlds,firstLiftUpYForOlds)
        plotTitle='Distribution of first lift up for all young adults'
        self.helpDrawTargetFirstLiftUpPlot2D(plotTitle,pathHeaderForAllYoungAdults, targetForPlot_list, firstLiftUpXForYoungs,firstLiftUpYForYoungs)
        plotTitle='Distribution of relative first lift up for all old adults'
        self.helpDrawRelativeTargetFirstLiftUpPlot2D(plotTitle,pathHeaderForAllOldAdults,firstRelaLiftUpXForOlds,firstRelaLiftUpYForOlds)
        plotTitle = 'Distribution of relative first lift up for all young adults'
        self.helpDrawRelativeTargetFirstLiftUpPlot2D(plotTitle,pathHeaderForAllYoungAdults, firstRelaLiftUpXForYoungs,firstRelaLiftUpYForYoungs)

    def drawAllTargetFirstLiftUpPlot3D(self,path):

        fileForAllParticipants = path + 'All_First_Lift_Up_3D.csv'
        firstLiftUpXForOlds = []
        firstLiftUpYForOlds = []
        firstLiftUpZForOlds=[]
        firstLiftUpXForYoungs = []
        firstLiftUpYForYoungs = []
        firstLiftUpZForYoungs=[]


        # load all the liftUp and relative liftUp data
        with open(fileForAllParticipants) as f:
            f_csv = csv.reader(f)
            next(f_csv)
            for row in f_csv:
                if float(row[0]) < 200:
                    firstLiftUpXForOlds.append(float(row[1]))
                    firstLiftUpYForOlds.append(float(row[2]))
                    firstLiftUpZForOlds.append(float(row[3]))

                else:
                    firstLiftUpXForYoungs.append(float(row[1]))
                    firstLiftUpYForYoungs.append(float(row[2]))
                    firstLiftUpZForYoungs.append(float(row[3]))

        # load all the target data
        fileForAllTargets = path + 'All_Target_3D.csv'

        with open(fileForAllTargets) as f:

            f_csv = csv.reader(f)
            next(f_csv)
            targetForPlot3D_list = []
            for row in f_csv:
                targetForPlot3D_list.append(TargetForPlot3D(float(row[0]), float(row[1]), float(row[2]),float(row[3])))
        plotTitle='Distribution of 3D first lift up of all old adults'
        self.helpDrawTargetFirstLiftUpPlot3D(plotTitle,pathHeaderForAllOldAdults, targetForPlot3D_list, firstLiftUpXForOlds,firstLiftUpYForOlds,firstLiftUpZForOlds)
        plotTitle='Distribution of 3D first lift up of all young adults'
        self.helpDrawTargetFirstLiftUpPlot3D(plotTitle,pathHeaderForAllYoungAdults, targetForPlot3D_list, firstLiftUpXForYoungs,firstLiftUpYForYoungs,firstLiftUpZForYoungs)


    def helpDrawTargetFirstLiftUpPlot2D(self,plotTitle,pathForPlot,targetForPlot_list,liftUpX_list,liftUpY_list):

        # draw the picture
        # we need to make the scale of x and y equal
        plt.figure(figsize=(5, 5), dpi=100)
        plt.title(plotTitle)
        matplotlib.rcParams.update({'font.size': 10})

        for t in targetForPlot_list:
            plt.scatter(t.x, t.y, c='c', alpha=1, marker='o', s=t.size, edgecolors='black')
        plt.scatter(liftUpX_list, liftUpY_list, c='r', alpha=1, marker='o', s=30, edgecolors='black')
        plt.xlabel('First Lift Up X(mm)')
        plt.ylabel('First Lift Up Y(mm)')
        plt.legend()
        plt.grid(True)
        plt.savefig(pathForPlot + plotTitle + '.png')

    def helpDrawTargetFirstLiftUpPlot3D(self, plotTitle,pathForPlot, targetForPlot3D_list, firstLiftUpX_list, firstLiftUpY_list,firstLiftUpZ_list):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # ax=self.create3DPlots()
        # draw the tablet plane
        X, Y, Z = self.drawTabletPlane()
        ax.scatter(X, Y, Z, c='c', alpha=0.1, marker='o', s=1)
        for t in targetForPlot3D_list:
            ax.scatter(t.x, t.y, t.z, c='r', label='target', alpha=1, marker='o', s=t.size, edgecolors='black')
        ax.scatter(firstLiftUpX_list, firstLiftUpY_list, firstLiftUpZ_list, c='c', label='First Lift Up', alpha=1,
                   marker='o', s=30, edgecolors='black')
        ax.set_xlabel('x(mm)')
        ax.set_ylabel('y(mm)')
        ax.set_zlabel('z(mm)')
        matplotlib.rcParams.update({'font.size': 10})
        plt.title(plotTitle)
        plt.legend()
        plt.savefig(pathForPlot + plotTitle + '.png')

    # go through all the trials in one experiment
    # draw targets and each first lift up points
    # the target is represented with green color
    # where the lift up points are represented with red color
    def drawTargetFirstLiftUpPlot2D(self,pathForPlot):

        file = self.path + "PId_" + str(self.pid) + "_TwoDFittsData_External.csv"

        with open(file) as f:

            targetForPlot_list=[]

            liftUpX_list = []
            liftUpY_list = []
            rela_liftUpX_list=[] # relative to the target as the center
            rela_liftUpY_list=[]

            f_csv = csv.reader(f)
            for i in range(0, 10):  # skip the beginning
                next(f_csv)

            width=0

            for row in f_csv:

                if width == 0:
                    width = float(row[colNumAndroidWidth])
                    #print width
                    sizeOfTarget = 0
                    if abs(width - 4.88) < 0.5:
                        sizeOfTarget = 180
                    if abs(width - 7.22) < 0.5:
                        sizeOfTarget = 340
                    if abs(width - 9.22) < 0.5:
                        sizeOfTarget = 500
                    width=0

                targetX=float(row[colNumAndroidTargetX]) * PixelToM
                targetY=float(row[colNumAndroidTargetY]) * PixelToM
                targetForPlot=TargetForPlot2D(targetX,targetY,sizeOfTarget)

                if targetForPlot not in targetForPlot_list:
                    targetForPlot_list.append(targetForPlot)

                liftUpX=float(row[colNumAndroidFirstLiftUpX]) * PixelToM
                liftUpY=float(row[colNumAndroidFirstLiftUpY]) * PixelToM
                rela_liftUpX=startTwoCor.x*PixelToM+liftUpX-targetX
                rela_liftUpY=startTwoCor.y*PixelToM+liftUpY-targetY
                liftUpX_list.append(liftUpX)
                liftUpY_list.append(liftUpY)
                rela_liftUpX_list.append(rela_liftUpX)
                rela_liftUpY_list.append(rela_liftUpY)



            plotTitle='Distribution of 2D first lift up in PID_'+str(self.pid)+'_Experiment'
            self.helpDrawTargetFirstLiftUpPlot2D(plotTitle,pathForPlot,targetForPlot_list,liftUpX_list,liftUpY_list)
            plotTitle='Relative Distribution of 2D first lift up in PID_'+str(self.pid)+'_Experiment'
            self.helpDrawRelativeTargetFirstLiftUpPlot2D(plotTitle,pathForPlot,rela_liftUpX_list,rela_liftUpY_list)

            # append all the plot data in one file for further merged plots
            fileForAllFirstLiftUp2D=pathHeaderForAllParticipiants+'All_First_Lift_Up_2D.csv'
            if not os.path.exists(fileForAllFirstLiftUp2D):
                with open(fileForAllFirstLiftUp2D, 'w') as f:
                    w_csv = csv.writer(f)
                    headers=['PID','Lift_Up_X(mm)','Lift_Up_Y(mm)','Relative_Lift_Up_X(mm)','Relative_Lift_Up_Y(mm)']
                    w_csv.writerow(headers)
            else:
                with open(fileForAllFirstLiftUp2D, 'a') as f:
                    w_csv = csv.writer(f)
                    for i in range(len(rela_liftUpX_list)):
                        row=[self.pid,liftUpX_list[i],liftUpY_list[i],rela_liftUpX_list[i],rela_liftUpY_list[i]]
                        w_csv.writerow(row)

            # write the target data in a file for further merged plots

            fileForAllTargets2D=pathHeaderForAllParticipiants+'All_Target_2D.csv'

            with open(fileForAllTargets2D, 'w') as f:
                w_csv = csv.writer(f)
                headers = ['targetX(mm)','targetY(mm)','targetSize(mm)']
                w_csv.writerow(headers)
                for t in targetForPlot_list:
                    w_csv.writerow([t.x,t.y,t.size])

    # the distribution of lift up in the first attempt
    def drawTargetFirstLiftUpPlot3D(self,pathForPlot):

        fileandroid = self.path + "PId_" + str(self.pid) + "_TwoDFittsData_External.csv"
        firstLiftUpTime_list = []

        targetForPlot3D_list=[]

        # store 3D cors for first lift up
        firstLiftUpX_list = []
        firstLiftUpY_list = []
        firstLiftUpZ_list = []
        with open(fileandroid) as f:
            f_csv = csv.reader(f)
            for i in range(0, 10):  # skip the beginning
                next(f_csv)

            for row in f_csv:

                width = float(row[colNumAndroidWidth])
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
            sizeOfTarget = 0
            if abs(self.targetWidth - 4.88) < 0.5:
                sizeOfTarget = 60
            if abs(self.targetWidth - 7.22) < 0.5:
                sizeOfTarget = 160
            if abs(self.targetWidth - 9.22) < 0.5:
                sizeOfTarget = 300
            targetForPlot3D_list.append(TargetForPlot3D(self.targetX,self.targetY,self.targetZ,sizeOfTarget))
            #print firstLiftUpTime_list[i]
            loc = self.getFirstLiftUpCors(firstLiftUpTime_list[i])
            firstLiftUpX_list.append(float(self.frameArray[loc][colNumSplitX]))
            firstLiftUpY_list.append(float(self.frameArray[loc][colNumSplitY]))
            firstLiftUpZ_list.append(float(self.frameArray[loc][colNumSplitZ]))
            #print 'targetX', 'targetY', 'targetZ', 'firstLiftUpX', 'firstLiftUpY', 'firstLiftUpZ'
            #print self.targetX, self.targetY, self.targetZ, self.frameArray[loc][colNumSplitX], self.frameArray[loc][colNumSplitY], self.frameArray[loc][colNumSplitZ]

        plotTitle='Distribution of 3D first lift up in PID_'+str(self.pid)+"_Experiment"
        self.helpDrawTargetFirstLiftUpPlot3D(plotTitle,pathForPlot,targetForPlot3D_list,firstLiftUpX_list,firstLiftUpY_list,firstLiftUpZ_list)

        fileForFirstLiftUp3D=pathHeaderForAllParticipiants+'All_First_Lift_Up_3D.csv'
        if not os.path.exists(fileForFirstLiftUp3D):
            with open(fileForFirstLiftUp3D, 'w') as f:
                w_csv = csv.writer(f)
                headers = ['pid', 'firstLiftUpX(mm)', 'firstLiftUpY(mm)', 'firstLiftUpZ(mm)']
                w_csv.writerow(headers)
                for i in range(len(firstLiftUpX_list)):
                    w_csv.writerow([self.pid, firstLiftUpX_list[i], firstLiftUpY_list[i], firstLiftUpZ_list[i]])
        else:
            with open(fileForFirstLiftUp3D, 'a') as f:
                w_csv = csv.writer(f)
                for i in range(len(firstLiftUpX_list)):
                    w_csv.writerow([self.pid, firstLiftUpX_list[i], firstLiftUpY_list[i], firstLiftUpZ_list[i]])

        # write the target data in a file for further merged plots

        fileForAllTargets2D = pathHeaderForAllParticipiants + 'All_Target_3D.csv'

        with open(fileForAllTargets2D, 'w') as f:
            w_csv = csv.writer(f)
            headers = ['targetX(mm)', 'targetY(mm)','targetZ(mm)', 'targetSize(mm)']
            w_csv.writerow(headers)
            for t in targetForPlot3D_list:
                w_csv.writerow([t.x, t.y,t.z, t.size])


    # find the First Lift Up Cors in leap motion
    # find the closest timestamp
    def getFirstLiftUpCors(self, FirstLiftUpTimestamp):
        for i in range(len(self.frameArray)):
            curTime = float(self.frameArray[i][colNumSplitTimestamp])
            if curTime == FirstLiftUpTimestamp:
                return i
            if curTime > FirstLiftUpTimestamp:
                prev = float(self.frameArray[i - 1][colNumSplitTimestamp])
                if abs(prev - FirstLiftUpTimestamp) < abs(curTime - FirstLiftUpTimestamp):  # find the closest one
                    return i - 1
                else:
                    return i
        return len(self.frameArray) - 2  # if not found,the one before final LiftUp is the end of the submovement

    '''
    # not used any more
    def drawRelativeTargetFirstLiftUpPlot3D(self,pathForPlot):

        # get the index of firstLiftUp in android files
        fileandroid = self.path + "PId_" + str(self.pid) + "_TwoDFittsData_External.csv"
        colNumFirstLiftUp = 20

        firstLiftUpTimeList=[] # store the timestamp for all the first lift up of frames in a trial

        with open(fileandroid) as f:

            f_csv = csv.reader(f)

            for i in range(0, 10):  # skip the beginning
                next(f_csv)

            for row in f_csv:
                firstLiftUpTimeList.append(float(row[colNumFirstLiftUp]))  # first lift up timestamp


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
            width = float(self.frameArray[0][colNumSplitWidth])
            sizeOfTarget = 0
            if abs(width - 4.88) < 0.5:
                sizeOfTarget = 250
            if abs(width - 7.22) < 0.5:
                sizeOfTarget = 600
            if abs(width - 9.22) < 0.5:
                sizeOfTarget = 1000

            index = self.getFirstLiftUpCors(firstLiftUpTimeList[i])  # get the index of the first lift up frame

            firstLiftUpX_list.append(float(self.frameArray[index][colNumSplitX]) - self.targetX)  # frameArray[loc] is the first Lift Up frame.Get the first List Up X cors.Then get the relative X
            firstLiftUpY_list.append(float(self.frameArray[index][colNumSplitY]) - self.targetY)
            firstLiftUpZ_list.append(float(self.frameArray[index][colNumSplitZ]) - self.targetZ)

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(firstLiftUpX_list, firstLiftUpY_list, firstLiftUpZ_list, c='r', label='First Lift Up', alpha=1,marker='o', s=30, edgecolors='black')
            ax.scatter(targetX_list, targetY_list, targetZ_list, c='c', label='target', alpha=1, marker='o', s=sizeOfTarget, edgecolors='black')

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
     '''
    def helpDrawRelativeTargetFirstLiftUpPlot2D(self,plotTitle, pathForPlot,rela_LiftUpX_list,rela_LiftUpY_list):
        # we need to make the scale of x and y equal
        plt.figure(figsize=(5, 5), dpi=100)
        plt.xlim(85, 95)
        plt.ylim(56, 66)
        plt.title(plotTitle)
        targetX_list=[startTwoCor.x*PixelToM] # view target as the center
        targetY_list=[startTwoCor.y*PixelToM]
        plt.scatter(targetX_list, targetY_list, c='r', alpha=1, marker='o', s=20,edgecolors='black')
        plt.scatter(rela_LiftUpX_list, rela_LiftUpY_list, c='c', alpha=1, marker='o', s=30, edgecolors='black')
        plt.xlabel('First Lift Up X(mm)')
        plt.ylabel('First Lift Up Y(mm)')
        plt.legend()
        plt.grid(True)
        plt.savefig(pathForPlot + plotTitle + '.png')
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
            startPathThreeCor = ThreeCorPoint(float(self.frameArray[0][colNumSplitX]) + self.offset3DX,
                                              float(self.frameArray[0][colNumSplitY]) + self.offset3DY,
                                              float(self.frameArray[0][colNumSplitZ]) + self.offset3DZ)

            self.projectedStartPathThreeCor = LocationInProjectedPlane(
                startPathThreeCor)  # project it in a system that tablet is vertical to the ground

            endPathThreeCor = ThreeCorPoint(float(self.frameArray[self.numberFrame - 1][colNumSplitX]) + self.offset3DX,
                                            float(self.frameArray[self.numberFrame - 1][colNumSplitY]) + self.offset3DY,
                                            float(self.frameArray[self.numberFrame - 1][colNumSplitZ]) + self.offset3DZ)

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
                pathThreeCor = ThreeCorPoint(float(self.frameArray[i][colNumSplitX]) + self.offset3DX,
                                             float(self.frameArray[i][colNumSplitY]) + self.offset3DY,
                                             float(self.frameArray[i][colNumSplitZ]) + self.offset3DZ)
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







