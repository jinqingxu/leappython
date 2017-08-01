#author:Irene
#find the best matched record from leap motion file for trials and output as files
import csv
import math

# 3D position
class ThreeCorPoint:
    x=0
    y=0
    z=0
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

class TwoCorPoint:
    x=0
    y=0
    def __init__(self, x, y):
        self.x=x
        self.y=y

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





#a global array to store data from leap motion
leapdata=[]
#a global array to store data from android
androiddata=[]
pid=0
#find the leap record with best timestamp_match of start
def best_match_start(stime,offset):
    for i in range(offset,len(leapdata)):
        if leapdata[i][2]>=stime: #the matched_timestamp is after the stime
            return i #return the matched index

# find the leap record with best timestamp_match of first_lift_up
def best_match_end(etime,offset):
    for i in range(offset, len(leapdata)):
        if leapdata[i][2] > etime: #the matched_timestamp is before etime,so find the first record that is after etime and return its previous one
            return i-1  #return the matched index
        elif leapdata[i][2]==etime:
            return i  #the exact matched

#write the split data into files
def split_and_write(begin,end,pid,block,trial,headers):
    file='/Users/irene/Desktop/data/split3/Pid_'+pid+'_Trial_'+trial+'.csv' #one trial matches one file
    with open(file, 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        for i in range(begin,end+1):#from begin to end
            newdata=[]
            newdata.append(pid)
            newdata.append(block)
            newdata.append(trial)
            newdata.extend(leapdata[i])
            f_csv.writerow(newdata)
    f.close()


def process():
    file1='/Users/irene/Desktop/data/Data from LEAPtest_results_PID_127_Frame.csv' #leap data
    file2='/Users/irene/Desktop/data/PId_127_2D_FittsDetailedTrialData_External.csv' #android data
    pid=(file2.split('_'))[1]
    headers=[]
    #read leap data
    with open(file1) as f:
        f_csv = csv.reader(f)
        for i in range(0,4):#skip the beginning
            next(f_csv)
        headers=next(f_csv)#get headers of csv
        headers2=['PID','Block','Trial']
        headers2.extend(headers)
        i=0
        for row in f_csv:
            leapdata.append(row)
    #read android data
    with open(file2) as f:
        # offset records the offset index of the visited data from leap motion so that we do not need to scan the leap data from begining
        offset = 0
        f_csv = csv.reader(f)
        for i in range(0,10):
            next(f_csv) #skip the beginning
        k=0
        for row in f_csv:
            stime=row[37] #row[34] is the start timestamp
            etime=row[38] #row[28] is the first_lift_up timestamp
            trial=str(k)
            block=0
            offset=best_match_start(stime,offset)
            begin=offset #the begin index of the split data
            offset=best_match_end(etime,offset+1)#the next scan should begin at the last_matched_index add 1
            end=offset #the end index of the split data
            split_and_write(begin,end,pid,block,trial,headers2)
            k=k+1


#get the mean x,y,z for each split data
def get_mean(pid):
    position3D=[]
    for i in range(0,5):
        file='/Users/irene/Desktop/data/split3/Pid_'+str(pid)+'_Trial_'+str(i)+'.csv'
        with open(file) as f:
            f_csv = csv.reader(f)
            next(f_csv)
            sum_x=0.0
            sum_y=0.0
            sum_z=0.0
            k=0
            for row in f_csv:
                sum_x+=float(row[6])
                sum_y+=float(row[7])
                sum_z+=float(row[8])
                k=k+1
            current=ThreeCorPoint(sum_x/(k+0.0),sum_y/(k+0.0),sum_z/(k+0.0))
            position3D.append(current)
    return position3D

#calculate the distance of the 5 points
def calculate_distance_3D_2D(position3D):
    distancesFor3D=[]
    for i in range(0,len(position3D)):
        start=position3D[i]
        for j in range(i+1,len(position3D)):
            end=position3D[j]
            dis=math.sqrt(math.pow(start.x-end.x,2)+math.pow(start.y-end.y,2)+math.pow(start.z-end.z,2))
            currentd=Distance(i,j,start.x,start.y,start.z,end.x,end.y,end.z,dis)
            distancesFor3D.append(currentd)
    return distancesFor3D










#process()
pid=127
position3D=get_mean(pid)
distancesFor3D=calculate_distance_3D_2D(position3D)


