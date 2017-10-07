#author:Irene

# calculate the difference between the calculated distance from start to end  and the real amplitude

import csv

from SpaceUtils import calculate_3D_Dis_Of_Two_Points


from GlobalVariables import *




from FileUtils import getSortedSplitFile

# 3D point
class ThreeCorPoint:
    x=0
    y=0
    z=0
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

# this class is used to store the caluclated distance and its error
class Dis_leap_android:

    block=0
    trial=0
    amplitude=0 # the real distance from start to target
    width=0 # the diameter of the target
    direction=0 # the direction of the target
    distance=0 # the calculated distance
    difference=0 # the error compared to the amplitude
    abs_difference=0 # the absoulte error

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

    startPointIndex=0 # the index of the start point,that is which row is the start of the path
    endPointIndex=0 # the index of the end point,that is which row is the end of the path
    startXCor=0.0
    startYCor=0.0
    startZCor=0.0
    endXCor=0.0
    endYCor=0.0
    endZCor=0.0
    dis=0.0 # the calculated distance

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

# get the min(l),max(l),avergae(l),difference of min and max
def get_min_max_mean_deviation_from_list(l):

    # if the list is empty,just return zero
    if len(l)==0:
        return 0,0,0,0

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

# write PID_XXX_Dis_Difference_Android_Leap.csv
def write_dis_difference(pid,pathForResult,pathForData):

    file2 = pathForData + 'PID_' + str(pid) + '_TwoDFittsData_External.csv'  # android data
    # headers for the new written file
    new_headers=['Block','Trial','Amplitude(mm)','Width(mm)','Direction','Start TipX(mm)','End TipX(mm)','Distance(mm)','Difference(mm)','AbsDifference(mm)','AbsDiffX(mm)','AbsDiff_Dis_X(mm)']
    file3 = pathForResult + 'PID_' + str(pid) + '_DIS_Difference_Android_Leap.csv' # the new file
    difference_dis_list=[] # record the difference between the calculated distance and amplitude
    absolute_difference_dis_list=[]  # record the absolute difference between the calculated distance and amplitude
    absolute_difference_X_list=[] # record the absolute difference of startX and endX
    absolute_difference_Dis_X_list=[] # record the difference between the distance calculated by x,y,z and the distance calculated only by x

    with open(file3, 'w') as f:
        w_csv = csv.writer(f)
        w_csv.writerow(new_headers)
        #get android data
        with open(file2) as f:
            f_csv = csv.reader(f)
            for i in range(0, 10):  # skip the beginning
                next(f_csv)

            # android data:Block,Trial,Amplitude,Width,Direction
            datas=[] #  two-dimensional array,one record means data of one trail
            for row in f_csv:
                difdata=[]
                difdata.append(row[colNumAndroidBlock])  # block
                difdata.append(row[colNumAndroidTrial])  # trial
                difdata.append(row[colNumAndroidAmplitude])  # amplitude in mm
                difdata.append(row[colNumAndroidWidth])  # width in mm
                difdata.append(row[colNumAndroidDirection])  # direction
                datas.append(difdata)
            path2=pathForData+'split/'
            files=getSortedSplitFile(path2,pid)
            for i in range(len(datas)):
                f = open(path2 + files[i], "r")
                length = len(f.readlines())  # get the length of the csv file
                with open(path2 + files[i]) as f:
                    f_csv = csv.reader(f)
                    next(f_csv)  # skip headers of csv
                    k = 1  # begin with the second line
                    # it's necessary to use a loop since f_csv is not an array but a type of csv_reader
                    # so we can not go through the f_csv
                    for row in f_csv:
                        if k == 1:
                            firstx = float(row[colNumSplitX])
                            firsty = float(row[colNumSplitY])
                            firstz = float(row[colNumSplitZ])
                        if k == length - 1:
                            endx = float(row[colNumSplitX])
                            endy = float(row[colNumSplitY])
                            endz = float(row[colNumSplitZ])
                        k = k + 1
                    # "firstx",firstx,"endx",endx
                    dis = calculate_3D_Dis_Of_Two_Points(firstx, firsty, firstz, endx, endy, endz)
                    difference = dis - float(datas[i][2])  # dis minus amplitude(mm)
                    absDiffX = abs(firstx - endx)
                    absDiff_Dis_X = abs(absDiffX - dis)
                    absDiff_Amplitude_X = abs(absDiffX - float(datas[i][2]))
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
        # get the min max average and deviation value
        min_d,max_d,average_d,deviation_d=get_min_max_mean_deviation_from_list(difference_dis_list)
        min_abs_d,max_abs_d,average_abs_d,deviation_abs_d=get_min_max_mean_deviation_from_list(absolute_difference_dis_list)
        min_abs_x,max_abs_x,average_abs_x,deviation_abs_x=get_min_max_mean_deviation_from_list(absolute_difference_X_list)
        min_abs_rx,max_abs_rx,average_abs_rx,deciation_abs_rx=get_min_max_mean_deviation_from_list(absolute_difference_Dis_X_list)
        for i in range(0,3):
            statistic = []
            for j in range(0,7):
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
def statistic_combination(pid,pathForResult,pathForData):

    dis_list = [] # the statistic data list

    file=pathForResult+'PID_'+str(pid)+'_DIS_Difference_Android_Leap.csv' # append the result at the bottom of the statistic file

    with open(file) as f:
        length=len(f.readlines())-4 # remove the header,the min,max,average in the bottom

    with open(file) as f:
        f_csv = csv.reader(f)
        next(f_csv)  # skip the headers
        j=0
        for row in f_csv:
            if j==length: # do not include the min,max,average value in the dis_list
                break
            tmp_dis=Dis_leap_android(row[colNumDisBlock],row[colNumDisTrial],row[colNumDisAmplitude],row[colNumDisWidth],row[colNumDisDirection],row[colNumDisDistance],row[colNumDisDifference],row[colNumDisAbsDifference])
            dis_list.append(tmp_dis)
            j=j+1

    # to find the min,max abs_difference of each combination
    # we can first sort the list with the priority of amplitude,width,direction and abs_difference
    # then the same combination will come together as a group
    # so the first one in the group is the min
    # and the last one in the group is the max
    dis_list=sorted(dis_list,dis_cmp)

    # suppose the combination with the same amplitude,width and direction is a group
    # each group will occur only once in one block
    with open(file, 'a') as f2: # append in the end of the original statistic file
        w_csv = csv.writer(f2)
        empty=[' ',' ', ' '] # an empty line
        w_csv.writerow(empty) # write an empty line in the beginning
        headers=['amplitude(mm)','width(mm)','direction','minAbsDifference(mm)','maxAbsDifference(mm)','avgAbsDifference(mm)']
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



# sort the list with the priority of amplitude,width,direction and abs_difference
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
'''
# the range of x is from -6 to 6
# the accurate value for y is 66,for z is -87.85
pid=851
write_dis_difference(pid)
statistic_combination(pid)
'''



