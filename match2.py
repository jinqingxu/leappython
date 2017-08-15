#author:Irene
#find the best matched record from leap motion file for trials and output as files
import csv
import math
import os
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

# 2D point
class TwoCorPoint:
    x=0
    y=0
    def __init__(self, x, y):
        self.x=x
        self.y=y

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

#a global array to store data from leap motion
leapdata=[]

#a global array to store data from android
androiddata=[]

# 1 pixel = 0.0794 mm
PixelToM=0.0794

Pi=3.1415926

# rulers means the real distance of the five points measured by rulers
#they are dis12,dis13,dis14,dis15,dis23,dis24,dis25,dis34,dis35,dis45
rulers=[40,40,40,40,56.6,80,56.56,56.56,80,56.56]

#find the leap record with best timestamp_match of start
def best_match_start(stime,offset):
    for i in range(offset,len(leapdata)):
        if leapdata[i][2]>=stime: #the matched_timestamp is after or equal to the stime
            return i #return the matched index of leap data
    return -1 # not found

# find the leap record with best timestamp_match of first_lift_up
def best_match_end(etime,offset):
    for i in range(offset, len(leapdata)):
        if leapdata[i][2] > etime: #the matched_timestamp is before etime,so find the first record that is after etime and return its previous one
            return i-1  #return the matched index
        elif leapdata[i][2]==etime:
            return i  #the exact matched of leap data
    return -1 # not found

#write the split data into files
def split_and_write(begin,end,pid,block,trial,headers,amplitude,width,direction):
    file=path+'split/'+'PID_'+str(pid)+'_Block_'+block+'_Trial_'+trial+'.csv' #one trial matches one file
    with open(file, 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        for i in range(begin,end+1):#from begin to end
            newdata=[]
            newdata.append(pid)
            newdata.append(block)
            newdata.append(trial)
            newdata.append(amplitude)
            newdata.append(width)
            newdata.append(direction)
            newdata.extend(leapdata[i])#data from leap motion
            f_csv.writerow(newdata)
    f.close()

# split the data from leap motion with the timstamp from android file
def process_split(pid,mode):
    file1=path+'Data from LEAPtest_results_PID_'+str(pid)+'_Frame.csv' #leap data
    file2=''
    if mode=='redcross':# for test experiment
        file2=path+'PID_'+str(pid)+'_FingerCalibData_Internal.csv'
    else:   # for real experiment
        file2=path+'PID_'+str(pid)+'_TwoDFittsData_External.csv' #android data
    headers=[] # for headers of the csv file
    #read leap data
    with open(file1) as f:
        f_csv = csv.reader(f)
        for i in range(0,4):#skip the beginning
            next(f_csv)
        headers=next(f_csv)#get headers of csv
        headers2=['PID','Block','Trial','Amplitude(mm)','Width(mm)','Direction']
        headers2.extend(headers) # headers2 is for the result file
        for row in f_csv:
            leapdata.append(row)
    #read android data
    with open(file2) as f:
        # offset records the offset index of the visited data from leap motion so that we do not need to scan the leap data from begining
        offset = 0
        f_csv = csv.reader(f)
        for i in range(0,10):
            next(f_csv) # skip the beginning
        for row in f_csv:
            stime=row[offsetStartTime] # the start timestamp
            etime=row[offsetFinalLiftUp] #  is the final_lift_up timestamp
            block = row[offsetBlock]
            trial = row[offsetTrial]
            amplitude=row[offsetAmplitude]
            width=row[offsetWidth]
            direction=row[offsetDirection]
            offset=best_match_start(stime,offset)
            if offset==-1:
                return
            begin=offset # the begin index of the split data
            offset=best_match_end(etime,offset+1) # the next scan should begin at the last_matched_index add 1
            if offset==-1:
                return
            end=offset #the end index of the split data
            split_and_write(begin,end,pid,block,trial,headers2,amplitude,width,direction)

#get the mean x,y,z for each split data
#that represents the 3D cors of each trial
def get_mean_from_split_files(pid,num):
    position3D=[]
    for i in range(0,5): # there are five measure points
        file=path+'Data from LEAPtest_results_PID_'+str(pid+i)+'_Frame.csv'
        a = open(file, "r")
        #print len(a.readlines())
        with open(file) as f:
            f_csv = csv.reader(f)
            for i in range(0, 5):
                next(f_csv)  # skip the beginning
            sum_x=0.0
            sum_y=0.0
            sum_z=0.0
            k=0
            for row in f_csv:
                sum_x+=float(row[offsetLeapX])
                sum_y+=float(row[offsetLeapY])
                sum_z+=float(row[offsetLeapZ])
                k=k+1
            current=ThreeCorPoint(sum_x/(k+0.0),sum_y/(k+0.0),sum_z/(k+0.0))
            position3D.append(current)
    return position3D

#calculate the distance of each point in the list with others
#for example,if there are points 1,2,3,4,5
#the function returns dis12,dis13,dis14,dis15,dis23,dis24,dis25,dis34,dis35,dis45
def calculate_distance_3D_Of_List(position3D):
    distancesFor3D=[]
    for i in range(0,len(position3D)):
        start=position3D[i]
        for j in range(i+1,len(position3D)):
            end=position3D[j]
            dis=math.sqrt(math.pow(start.x-end.x,2)+math.pow(start.y-end.y,2)+math.pow(start.z-end.z,2))
            currentd=Distance(i,j,start.x,start.y,start.z,end.x,end.y,end.z,dis)
            distancesFor3D.append(currentd)
    return distancesFor3D

# find the 3D cors for the 2D cors point on ipad
# the 2D cors are in pixels unit
def TwoCorToThreeCor(currentTwoCor):
    #the start point is the center of the ipad
    startThreeCor = ThreeCorPoint(-2.33, 44.395, -33.421)
    startTwoCor = TwoCorPoint(1024, 720)
    # * PixelToM change the unit from pixel to mm
    ChangeDis = math.sqrt(math.pow(startTwoCor.x - currentTwoCor.x, 2) + math.pow(startTwoCor.y - currentTwoCor.y, 2))*PixelToM
    ChangeX = abs(currentTwoCor.x - startTwoCor.x)*PixelToM # X's location change in 2D is the same as that in 3D
    Change2DY=abs(currentTwoCor.y-currentTwoCor.y)*PixelToM # Change2Y means the  location change of Y axis in the 2D plane
    ChangeY =  Change2DY* math.sin(Pi / 4) # the angle of the plane is 45 degree
    ChangZ =  Change2DY* math.cos(Pi / 4)
    # let the center point as base point, find the taget point's direction
    # right-up,left-up,left-down,right-down
    # right
    if currentTwoCor.x>startTwoCor.x:
        #right-up
        if currentTwoCor.y<startTwoCor.y:
            # x++ y++ z--
            newX=startThreeCor.x+ChangeX
            newY=startThreeCor.y+ChangeY
            newZ=startThreeCor.z-ChangZ
        #right-down
        else:
            # x++ y-- z++
            newX = startThreeCor.x + ChangeX
            newY = startThreeCor.y - ChangeY
            newZ = startThreeCor.z + ChangZ
    #left
    else:
        # left-up
        if currentTwoCor.y < startTwoCor.y:
            # x-- y++ z--
            newX = startThreeCor.x - ChangeX
            newY = startThreeCor.y + ChangeY
            newZ = startThreeCor.z - ChangZ
        # left-down
        else:
            # x-- y-- z++
            newX = startThreeCor.x - ChangeX
            newY = startThreeCor.y - ChangeY
            newZ = startThreeCor.z + ChangZ

    target=ThreeCorPoint(newX,newY,newZ)
    return target

# write file and print error of distances
def write_and_print_error(pid,distancesFor3D):
    file1 = path+'PID_' + str(pid) + '_DIS_error.csv'
    header=[ "StartIndex", "EndIndex", "RealDis(mm)", "CalDis(mm)","Error(mm)"]
    print 'StartIndex','EndIndex','RealDis(mm)','CalDis(mm)','Error(mm)'
    with open(file1, 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(header)
        for i in range(0, len(distancesFor3D)):
            data = []
            data.append(distancesFor3D[i].startPointIndex)
            data.append(distancesFor3D[i].endPointIndex)
            data.append(rulers[i]) # the real distance
            data.append(distancesFor3D[i].dis) # the calculated distance of data from leap motion
            data.append(distancesFor3D[i].dis-rulers[i])
            f_csv.writerow(data)
            print distancesFor3D[i].startPointIndex,
            print distancesFor3D[i].endPointIndex,
            print rulers[i],
            print distancesFor3D[i].dis,
            print distancesFor3D[i].dis-rulers[i]

# calculate the distance of two 3D points
def calculate_3D_Dis_Of_Two_Points(x1,y1,z1,x2,y2,z2):
    return math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2)+math.pow(z1-z2,2))

def print_min_mean_max_from_split_files(pid,num):
    lxs=[] # two-dimension array,one record means an array of x from a trial
    lys=[] # two-dimension array,one record means an array of y from a trial
    lzs=[] # two-dimension array,one record means an array of z from a trial
    for i in range(0,num):
        file=path+'/Data from LEAPtest_results_PID_'+str(pid+i)+'_Frame.csv'
        with open(file) as f:
            f_csv = csv.reader(f)
            for i in range(0, 4):  # skip the beginning
                next(f_csv)
            headers = next(f_csv)  # get headers of csv
            tmp_lx=[]
            tmp_ly=[]
            tmp_lz=[]
            for row in f_csv:
                tmp_lx.append(row[offsetLeapX])
                tmp_ly.append(row[offsetLeapY])
                tmp_lz.append(row[offsetLeapZ])
        lxs.append(tmp_lx)
        lys.append(tmp_ly)
        lzs.append(tmp_lz)
    for i in range(0,len(lxs)):
        print 'x'+str(i+1),
        print get_min_max_mean_deviation_from_list(lxs[i]) #one record means an array of x from a trial
        print 'y'+str(i+1),
        print get_min_max_mean_deviation_from_list(lys[i])
        print 'z'+str(i+1),
        print get_min_max_mean_deviation_from_list(lzs[i])

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

# write PID_XXX_Dis_Difference_Android_Leap
def write_dis_difference(pid):
    files = os.listdir(path+'/split')
    file2 = path + 'PID_' + str(pid) + '_TwoDFittsData_External.csv'  # android data
    new_headers=['Block','Trial','Amplitude(mm)','Width(mm)','Direction','Distance(mm)','Difference(mm)','Absolute_Difference(mm)'] # headers for the written file
    file3 = path + 'PID_' + str(pid) + '_DIS_Difference_Android_Leap.csv'
    difference_dis_list=[] # record the difference between the calculated distance and amplitude
    absolute_difference_dis_list=[]  # record the absolute difference between the calculated distance and amplitude
    with open(file3, 'w') as f:
        w_csv = csv.writer(f)
        w_csv.writerow(new_headers)
        #get android data
        with open(file2) as f:
            f_csv = csv.reader(f)
            for i in range(0, 10):  # skip the beginning
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
                if not os.path.isdir(file):  # not a directory
                    # a bug : if the pid is 888,files begin with pid 8881 will be taken into account
                    keys=file.split('_')
                    if str(pid) in keys:  # if the file begins with PID_xxx
                        print file
                        if i==len(datas):
                            break
                        f = open(path + '/split/' + file, "r")
                        length = len(f.readlines())  # get the length of the csv file
                        with open(path+'/split/'+file) as f:
                            f_csv = csv.reader(f)
                            headers = next(f_csv)  # get headers of csv
                            k = 1  # begin with the second line
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
                            dis = calculate_3D_Dis_Of_Two_Points(firstx, firsty, firstz, endx, endy, endz)
                            difference = dis - float(datas[i][2])  # dis minus amplitude(mm)
                            datas[i].append(dis)
                            datas[i].append(difference)
                            datas[i].append(abs(difference))
                            difference_dis_list.append(difference)
                            absolute_difference_dis_list.append(abs(difference))
                            w_csv.writerow(datas[i])
                        i=i+1
        min_d,max_d,average_d,deviation_d=get_min_max_mean_deviation_from_list(difference_dis_list)
        min_abs_d,max_abs_d,average_abs_d,deviation_abs_d=get_min_max_mean_deviation_from_list(absolute_difference_dis_list)
        for i in range(0,3):
            statistic = []
            for j in range(0,5):
                statistic.append(' ') # space
            if i==0:
                statistic.append('min')
                statistic.append(min_d)
                statistic.append(min_abs_d)
            if i==1:
                statistic.append('max')
                statistic.append(max_d)
                statistic.append(max_abs_d)
            if i==2:
                statistic.append('average')
                statistic.append(average_d)
                statistic.append(average_abs_d)
            w_csv.writerow(statistic)


# find the min,max,average abs_difference of all combinations of amplitude,width and direction
def statistic_combination(pid):
    dis_list = []
    numOfBlocks = 4
    file=path+'PID_'+str(pid)+'_DIS_Difference_Android_Leap.csv'
    length=188
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
    groupNum=(length)/numOfBlocks
    # suppose the combination with the same amplitude,width and direction is a group
    # each group will occur only once in one block
    with open(file, 'a') as f2:
        w_csv = csv.writer(f2)
        empty=[' ',' ', ' ']
        w_csv.writerow(empty)
        headers=['amplitude','width','direction','min','max','avg']
        w_csv.writerow(headers)
        for i in range(0,groupNum):
            min_group=float(dis_list[i*numOfBlocks].abs_difference)
            max_group=float(dis_list[i*numOfBlocks+numOfBlocks-1].abs_difference)
            sum_group=0
            # find the average
            for k in range(0,numOfBlocks):
                tmp_dis=float(dis_list[i*numOfBlocks+k].abs_difference)
                sum_group+=tmp_dis
                if tmp_dis<min_group:
                    min_group=tmp_dis
                if tmp_dis>max_group:
                    max_group=tmp_dis
            avg_group=sum_group/(numOfBlocks+0.0)
            outdata=[]
            outdata.append(dis_list[i*numOfBlocks].amplitude)
            outdata.append(dis_list[i*numOfBlocks].width)
            outdata.append(dis_list[i*numOfBlocks].direction)
            outdata.append(min_group)
            outdata.append(max_group)
            outdata.append(avg_group)
            w_csv.writerow(outdata)










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


spid=555
mode='circle' # redcross means test experiment,circle means real experiment
process_split(spid,mode)
write_dis_difference(spid)

statistic_combination(spid)
# for test data
# pid range from 641 to 645
#pid=641
#num=5
#position3D=get_mean_from_split_files(pid,num)
#print_min_mean_max_from_split_files(pid,num)
#distancesFor3D=calculate_distance_3D_Of_List(position3D) # ten distances for the 5 points
#write_and_print_error(distancesFor3D)

