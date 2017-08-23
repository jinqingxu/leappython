#author:Irene
#find the best matched record from leap motion file for trials and output as files
import csv
import math
import os
from SpaceUtils import calculate_3D_Dis_Of_Two_Points

# 3D point
class ThreeCorPoint:
    x=0
    y=0
    z=0
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

class Dis_leap_android:
    block=0
    trial=0
    amplitude=0
    width=0
    direction=0
    distance=0
    difference=0
    abs_difference=0
    def __init__(self,block,trial,amplitude,width,direction,distance,difference,abs_difference):
        self.block=block
        self.trial=trial
        self.amplitude=amplitude
        self.width=width
        self.direction=direction
        self.distance=distance
        self.difference=difference
        self.abs_difference=abs_difference


# distance between two 3D points
class Distance:
    startPointIndex=0
    endPointIndex=0
    startXCor=0.0
    startYCor=0.0
    startZCor=0.0
    endXCor=0.0
    endYCor=0.0
    endZCor=0.0
    dis=0.0
    def __init__(self,startPointIndex,endPointIndex,startXCor,startYCor,startZCor,endXCor,endYCor,endZCor,dis):
        self.startPointIndex=startPointIndex
        self.endPointIndex=endPointIndex
        self.startXCor=startXCor
        self.startYCor=startYCor
        self.startZCor=startZCor
        self.endXCor=endXCor
        self.endYCor=endYCor
        self.endZCor=endZCor
        self.dis=dis

# the index of data in android file
offsetStartTime = 15
offsetFinalLiftUp = 22
offsetBlock=2
offsetTrial=3
offsetAmplitude=5
offsetWidth=7
offsetDirection=8

# the index of data in leap file
offsetLeapX=3
offsetLeapY=4
offsetLeapZ=5

# the index of data in split file
offsetSplitX=9
offsetSplitY=10
offsetSplitZ=11

# the index of data in dif file
offsetDisBlock=0
offsetDisTrial=1
offsetDisAmplitude=2
offsetDisWidth=3
offsetDisDirection=4
offsetDisDistance=5
offsetDisDifference=6
offsetDisAbsDifference=7

#workpath
path = '/Users/irene/Documents/McGillUni/ACT_Research_Lab/Experiments/Motion Tracking Study/Experiment Data/'

# 1 pixel = 0.0794 mm(calculated by Irene)
# 1 pixel = 0.088194mm(from the website)
PixelToM=0.088194
Pi=3.1415926



# get the min(l),max(l),avergae(l),difference of min and max
def get_min_max_mean_deviation_from_list(l):
    min_l=float(l[0])
    max_l=float(l[0])
    sum_l=0
    for i in range(0,len(l)):
        if float(l[i])>max_l:
            max_l=float(l[i])
        if float(l[i])<min_l:
            min_l=float(l[i])
        sum_l+=float(l[i])
    return min_l, max_l, sum_l / (len(l) + 0.0),max_l-min_l

def file_cmp(x,y):
    key1=x.split('_')
    key2=y.split('_')
    block1=int(key1[3])
    block2=int(key2[3])
    trial1=int(key1[5][0:-4])
    trial2=int(key2[5][0:-4])
    if block1<block2:
        return -1
    if block1>block2:
        return 1
    if block1==block2:
        if trial1<trial2:
            return -1
        if trial1==trial2:
            return 0
        if trial1>trial2:
            return 1

# write PID_XXX_Dis_Difference_Android_Leap
def write_dis_difference(pid):
    files = os.listdir(path+'/split')
    files=files[1:len(files)]
    files=sorted(files,file_cmp)
    file2 = path + 'PID_' + str(pid) + '_TwoDFittsData_External.csv'  # android data
    new_headers=['Block','Trial','Amplitude(mm)','Width(mm)','Direction','Start TipX(mm)','End TipX(mm)','Distance(mm)','Difference(mm)','AbsDifference(mm)','AbsDiffX(mm)','AbsDiff_Dis_X(mm)'] # headers for the written file
    file3 = path + 'PID_' + str(pid) + '_DIS_Difference_Android_Leap.csv'
    difference_dis_list=[] # record the difference between the calculated distance and amplitude
    absolute_difference_dis_list=[]  # record the absolute difference between the calculated distance and amplitude
    absolute_difference_X_list=[] # record the absolute difference of startX and endX
    absolute_difference_Dis_X_list=[]
    with open(file3, 'w') as f:
        w_csv = csv.writer(f)
        w_csv.writerow(new_headers)
        #get android data
        with open(file2) as f:
            f_csv = csv.reader(f)
            for i in range(0, 9):  # skip the beginning
                next(f_csv)
            headers = next(f_csv)  # get headers of csv
            # android data:Block,Trial,Amplitude,Width,Direction
            datas=[] #  two-dimensional array,one record means data of one trail
            for row in f_csv:
                difdata=[]
                difdata.append(row[offsetBlock])  # block
                difdata.append(row[offsetTrial])  # trial
                difdata.append(row[offsetAmplitude])  # amplitude in mm
                difdata.append(row[offsetWidth])  # width in mm
                difdata.append(row[offsetDirection])  # direction
                datas.append(difdata)
            i=0 # index of trial
            # PID_xxx_Block_xxx_Trial_xxx.csv

            for file in files: # open all the file in the '/split' directory
                print file
                if not os.path.isdir(file):  # not a directory
                    # a bug : if the pid is 888,files begin with pid 8881 will be taken into account
                    keys=file.split('_')
                    if str(pid) in keys:  # if the file begins with PID_xxx
                        if i==len(datas):
                            break
                        f = open(path + '/split/' + file, "r")
                        length = len(f.readlines())  # get the length of the csv file
                        with open(path+'/split/'+file) as f:
                            f_csv = csv.reader(f)
                            headers = next(f_csv)  # get headers of csv
                            k = 1  # begin with the second line
                            # it's necessary to use a loop since f_csv is not an array but a type of csv_reader
                            # so we can not go through the f_csv
                            for row in f_csv:
                                if k == 1:
                                    firstx = float(row[offsetSplitX])
                                    firsty = float(row[offsetSplitY])
                                    firstz = float(row[offsetSplitZ])
                                if k == length - 1:
                                    endx = float(row[offsetSplitX])
                                    endy = float(row[offsetSplitY])
                                    endz = float(row[offsetSplitZ])
                                k = k + 1
                            # "firstx",firstx,"endx",endx
                            dis = calculate_3D_Dis_Of_Two_Points(firstx, firsty, firstz, endx, endy, endz)
                            difference = dis - float(datas[i][2])  # dis minus amplitude(mm)
                            absDiffX=abs(firstx-endx)
                            absDiff_Dis_X=abs(absDiffX-dis)
                            absDiff_Amplitude_X=abs(absDiffX-float(datas[i][2]))
                            datas[i].append(firstx)
                            datas[i].append(endx)
                            datas[i].append(dis)
                            datas[i].append(difference)
                            datas[i].append(abs(difference))
                            datas[i].append(absDiffX)
                            datas[i].append(absDiff_Dis_X)
                            # used for further calculation of min,max,average
                            difference_dis_list.append(difference)
                            absolute_difference_dis_list.append(abs(difference))
                            absolute_difference_X_list.append(absDiffX)
                            absolute_difference_Dis_X_list.append(absDiff_Dis_X)
                            w_csv.writerow(datas[i])
                        i=i+1
        min_d,max_d,average_d,deviation_d=get_min_max_mean_deviation_from_list(difference_dis_list)
        min_abs_d,max_abs_d,average_abs_d,deviation_abs_d=get_min_max_mean_deviation_from_list(absolute_difference_dis_list)
        min_abs_x,max_abs_x,average_abs_x,deviation_abs_x=get_min_max_mean_deviation_from_list(absolute_difference_X_list)
        min_abs_rx,max_abs_rx,average_abs_rx,deciation_abs_rx=get_min_max_mean_deviation_from_list(absolute_difference_Dis_X_list)
        for i in range(0,3):
            statistic = []
            for j in range(0,5):
                statistic.append(' ') # space
            if i==0:
                statistic.append('min')
                statistic.append(min_d)
                statistic.append(min_abs_d)
                statistic.append(min_abs_x)
                statistic.append(min_abs_rx)
            if i==1:
                statistic.append('max')
                statistic.append(max_d)
                statistic.append(max_abs_d)
                statistic.append(max_abs_x)
                statistic.append(max_abs_rx)
            if i==2:
                statistic.append('average')
                statistic.append(average_d)
                statistic.append(average_abs_d)
                statistic.append(average_abs_x)
                statistic.append(average_abs_rx)
            w_csv.writerow(statistic)



# find the min,max,average abs_difference of all combinations of amplitude,width and direction
def statistic_combination(pid,numberOfCombination):
    dis_list = []
    file=path+'PID_'+str(pid)+'_DIS_Difference_Android_Leap.csv'
    length=0
    with open(file) as f:
        length=len(f.readlines())-4 # remove the header , the min,max,average in the bottom
    with open(file) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)  # get headers of csv
        j=0
        for row in f_csv:
            if j==length:
                break
            tmp_dis=Dis_leap_android(row[offsetDisBlock],row[offsetDisTrial],row[offsetDisAmplitude],row[offsetDisWidth],row[offsetDisDirection],row[offsetDisDistance],row[offsetDisDifference],row[offsetDisAbsDifference])
            dis_list.append(tmp_dis)
            j=j+1
    dis_list=sorted(dis_list,dis_cmp)
    #for i in range(len(dis_list)):
        #print dis_list[i].amplitude,dis_list[i].width,dis_list[i].direction,dis_list[i].abs_difference
    # suppose the combination with the same amplitude,width and direction is a group
    # each group will occur only once in one block
    with open(file, 'a') as f2:
        w_csv = csv.writer(f2)
        empty=[' ',' ', ' '] # an empty line
        w_csv.writerow(empty)
        headers=['amplitude(mm)','width(mm)','direction','minAbsDiff(mm)','maxAbsDiff(mm)','avgAbsDiff(mm)']
        w_csv.writerow(headers)
        # initial
        prevAmplitude=dis_list[0].amplitude
        prevWidth=dis_list[0].width
        prevDirection=dis_list[0].direction
        min_group = float(dis_list[0].abs_difference)
        max_group = float(dis_list[0].abs_difference)
        sum_group = 0
        lenOfCombination = 0  # how many records are there in one combination
        for i in range(0,len(dis_list)):
            curAmplitude=dis_list[i].amplitude
            curWidth=dis_list[i].width
            curDirection=dis_list[i].direction
            if curAmplitude==prevAmplitude and curWidth==prevWidth and curDirection==prevDirection:
                lenOfCombination=lenOfCombination+1
                tmp_dis = float(dis_list[i].abs_difference)
                sum_group += tmp_dis
                if tmp_dis < min_group:
                    min_group = tmp_dis
                if tmp_dis > max_group:
                    max_group = tmp_dis
            if curAmplitude!=prevAmplitude or curWidth!=prevWidth or curDirection!=prevDirection or i==len(dis_list)-1: # the beginning of next combination
                #print "sum",sum_group
                #print "lenOfConbination",lenOfCombination
                avg_group = sum_group / (lenOfCombination + 0.0)
                outdata = []
                outdata.append(dis_list[i-1].amplitude)
                outdata.append(dis_list[i-1].width)
                outdata.append(dis_list[i-1].direction)
                outdata.append(min_group)
                outdata.append(max_group)
                outdata.append(avg_group)
                w_csv.writerow(outdata)
                min_group = float(dis_list[i].abs_difference)
                max_group = float(dis_list[i].abs_difference)
                sum_group = float(dis_list[i].abs_difference)
                lenOfCombination=1
                prevAmplitude=curAmplitude
                prevWidth=curWidth
                prevDirection=curDirection



# to find the min,max abs_difference of each combination
# we can first sort the list with the priority of amplitude,width,direction and abs_difference
# then the same combination will come together as a group
# so the first one in the group is the min
# and the last one in the group is the max
def dis_cmp(x,y):
    if x.amplitude<y.amplitude:
        return -1
    if x.amplitude>y.amplitude:
        return 1
    if x.amplitude==y.amplitude:

        if x.width<y.width:
            return -1
        if x.width>y.width:
            return 1
        if x.width==y.width:
            if x.direction<y.direction:
                return -1
            if x.direction>y.direction:
                return 1
            if x.direction==y.direction:
                return 0


# the range of x is from -6 to 6
# the accurate value for y is 66,for z is -87.85
pid=890
numberOfCombination=2
write_dis_difference(pid)
statistic_combination(pid,numberOfCombination)



