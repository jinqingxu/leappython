#author:Irene
#find the best matched record from leap motion file for trials and output as files
import csv
import math
import os
# android data
from GlobalVariables import *


import shutil

class LeapTimeStamp:

    block=0
    trial=0
    leapStartTimeStamp=0
    leapFirstLiftUpTimeStamp=0
    leapFinalLiftUpTime=0

    def __init__(self,block,trial,leapStartTimeStamp,leapFirstLiftUpTimeStamp,leapFinalLiftUpTime):
        self.block=block
        self.trial=trial
        self.leapStartTimeStamp=leapStartTimeStamp
        self.leapFirstLiftUpTimeStamp=leapFirstLiftUpTimeStamp
        self.leapFinalLiftUpTime=leapFinalLiftUpTime



#a global array to store data from leap motion
leapdata=[]

#a global array to store data from android
androiddata=[]

#find the leap record with best timestamp_match of start
def best_match_start(stime,index):
    for i in range(index,len(leapdata)):
        if leapdata[i][colNumLeapTimeStamp]>=stime: #the matched_timestamp is after or equal to the stime
            return i #return the matched index of leap data
    return -1 # not found

# find the leap record with best timestamp_match of first_lift_up
def best_match_end(etime,index):
    for i in range(index, len(leapdata)):
        if leapdata[i][colNumLeapTimeStamp] > etime: #the matched_timestamp is before etime,so find the first record that is after etime and return its previous one
            return i-1  #return the matched index
        elif leapdata[i][colNumLeapTimeStamp]==etime:
            return i  #the exact matched of leap data
    return -1 # not found

def best_match_firstLiftUp(ftime,index):
    for i in range(index, len(leapdata)):
        if leapdata[i][colNumLeapTimeStamp] > ftime:  # the matched_timestamp is before etime,so find the first record that is after etime and return its previous one
            return i - 1  # return the matched index
        elif leapdata[i][colNumLeapTimeStamp] == ftime:
            return i  # the exact matched of leap data
    return -1  # not found

#write the split data into files
def split_and_write(begin,end,pid,block,trial,headers,amplitude,width,direction,path):
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

def writeLeapTimeStamp(path,pid,leapTimeStamp_list):

    leapTimeStampFile = path + 'PID_' + str(pid) + '_Leap_TimeStamp_Data.csv'  # for further use, those data will be added into the measurement file
    headers=['block','trial','startTimeStamp','firstLiftUpTimeStamp','finalLiftUpTimeStamp']

    with open(leapTimeStampFile, 'w') as f:

        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        for l in leapTimeStamp_list:
            data=[l.block,l.trial,l.leapStartTimeStamp,l.leapFirstLiftUpTimeStamp,l.leapFinalLiftUpTime]
            f_csv.writerow(data)






# split the data from leap motion with the timstamp from android file
def process_split(pid,path):

    leapTimeStamp_list=[]
    #shutil.rmtree(path+'split/')
    if not os.path.exists(path+'split/'):
        os.mkdir(path+'split/')
    file1=path+'PID_'+str(pid)+'_Data_from_LEAPtest_results_Frame.csv' #leap data
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
        # index records the current index of the visited data from leap motion so that we do not need to scan the leap data from begining
        index = 0
        f_csv = csv.reader(f)
        for i in range(0,10):
            next(f_csv) # skip the beginning
        for row in f_csv:
            stime=row[colNumAndroidStartTime] # the start timestamp
            etime=row[colNumAndroidFinalLiftUp] #  is the final_lift_up timestamp
            ftime=row[colNumAndroidFirstLiftUpTimeStamp] # is the first_lift_up timestamp
            block = row[colNumAndroidBlock]
            trial = row[colNumAndroidTrial]
            amplitude=row[colNumAndroidAmplitude]
            width=row[colNumAndroidWidth]
            direction=row[colNumAndroidDirection]
            # to find the best matched start index
            index=best_match_start(stime,index)
            if index==-1:
                return
            begin=index # the begin index of the split data
            if ftime==etime:
                # to find the best matched end index
                # the next scan should begin at the last_matched_index add 1
                index = best_match_end(etime, index + 1)
                if index == -1:
                    return
                end = index  # the end index of the split data
                firstLiftUpIndex=end
            else:
                index = best_match_firstLiftUp(ftime, index)
                firstLiftUpIndex = index
                # to find the best matched end index
                # the next scan should begin at the last_matched_index add 1
                index = best_match_end(etime, index + 1)
                if index == -1:
                    return
                end = index  # the end index of the split data


            # use the start and end loc to split the data
            split_and_write(begin,end,pid,block,trial,headers2,amplitude,width,direction,path)

            # store the leap timeStamp
            leapTimeStamp=LeapTimeStamp(block,trial,leapdata[begin][colNumLeapTimeStamp],leapdata[firstLiftUpIndex][colNumLeapTimeStamp],leapdata[end][colNumLeapTimeStamp])
            leapTimeStamp_list.append(leapTimeStamp)

    writeLeapTimeStamp(path,pid,leapTimeStamp_list)


'''
pid=851
process_split(pid)
'''