import csv
import math
import os
from CalculateOfCircle import get_min_max_mean_deviation_from_list
from GlobalVariables import offsetLeapX
from GlobalVariables import offsetLeapY
from GlobalVariables import offsetLeapZ
from GlobalVariables import path
# 3D point
class ThreeCorPoint:
    x=0
    y=0
    z=0
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

# distance between two 3D points
class Distance:
    startPointIndex = 0
    endPointIndex = 0
    startXCor = 0.0
    startYCor = 0.0
    startZCor = 0.0
    endXCor = 0.0
    endYCor = 0.0
    endZCor = 0.0
    dis = 0.0
    def __init__(self, startPointIndex, endPointIndex, startXCor, startYCor, startZCor, endXCor, endYCor, endZCor, dis):
        self.startPointIndex = startPointIndex
        self.endPointIndex = endPointIndex
        self.startXCor = startXCor
        self.startYCor = startYCor
        self.startZCor = startZCor
        self.endXCor = endXCor
        self.endYCor = endYCor
        self.endZCor = endZCor
        self.dis = dis

# rulers means the real distance of the five points measured by rulers
# they are dis12,dis13,dis14,dis15,dis23,dis24,dis25,dis34,dis35,dis45
rulers = [40, 40, 40, 40, 56.6, 80, 56.56, 56.56, 80, 56.56]

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

# write file and print error of distances
def write_and_print_error(distancesFor3D):
    file1 = path+'RedCross_DIS_error.csv'
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

# for test data
# pid range from 641 to 645
pid=641
num=5
position3D=get_mean_from_split_files(pid,num)
print_min_mean_max_from_split_files(pid,num)
distancesFor3D=calculate_distance_3D_Of_List(position3D) # ten distances for the 5 points
write_and_print_error(distancesFor3D)