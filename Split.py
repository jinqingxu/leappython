#author:Irene
#find the best matched record from leap motion file for trials and output as files
import csv
import math
import os
# android data
from GlobalVariables import offsetAndroidStartTime
from GlobalVariables import offsetAndroidFinalLiftUp
from GlobalVariables import offsetAndroidBlock
from GlobalVariables import offsetAndroidTrial
from GlobalVariables import  offsetAndroidAmplitude
from GlobalVariables import  offsetAndroidWidth
from GlobalVariables import offsetAndroidDirection


import shutil



#a global array to store data from leap motion
leapdata=[]

#a global array to store data from android
androiddata=[]

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

# split the data from leap motion with the timstamp from android file
def process_split(pid,path):
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
        # offset records the offset index of the visited data from leap motion so that we do not need to scan the leap data from begining
        offset = 0
        f_csv = csv.reader(f)
        for i in range(0,10):
            next(f_csv) # skip the beginning
        for row in f_csv:
            stime=row[offsetAndroidStartTime] # the start timestamp
            etime=row[offsetAndroidFinalLiftUp] #  is the final_lift_up timestamp
            block = row[offsetAndroidBlock]
            trial = row[offsetAndroidTrial]
            amplitude=row[offsetAndroidAmplitude]
            width=row[offsetAndroidWidth]
            direction=row[offsetAndroidDirection]
            # to find the best matched start offset
            offset=best_match_start(stime,offset)
            if offset==-1:
                return
            begin=offset # the begin index of the split data
            # to find the best matched end offset
            # the next scan should begin at the last_matched_index add 1
            offset=best_match_end(etime,offset+1)
            if offset==-1:
                return
            end=offset #the end index of the split data
            # use the start and end offset to split the data
            split_and_write(begin,end,pid,block,trial,headers2,amplitude,width,direction,path)

'''
pid=851
process_split(pid)
'''