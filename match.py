#author:Irene
#find the best matched record from leap motion file for trials and output as files
import csv

#a global object to store data from leap motion
leapdata=[]

#find the leap record with best timestamp_match of start
def best_match_start(stime,offset):
    for i in range(offset,len(leapdata)):
        if leapdata[i][2]>=stime:#the matched_timestamp is after the stime
            return i #return the matched index

# find the leap record with best timestamp_match of first_lift_up
def best_match_end(etime,offset):
    for i in range(offset, len(leapdata)):
        if leapdata[i][2] > etime:#the matched_timestamp is before etime,so find the first record that is after etime and return its previous one
            return i-1  #return the matched index
        elif leapdata[i][2]==etime:
            return i  #the exact matched

#write the split data into files
def split_and_write(begin,end,block,trial,pid,headers):
    file='/Users/irene/Desktop/data/split_PID_136/Pid_'+pid+'_Block_'+block+'_Trial_'+trial+'.csv'#one trial matches one file
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
    file1='/Users/irene/Desktop/data/Data from LEAPtest_results_PID_136_Frame.csv' #leap data
    file2='/Users/irene/Desktop/data/PId_136_2D_FittsDetailedTrialData_External.csv' #android data
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
        for row in f_csv:
            stime=row[34] #row[34] is the start timestamp
            etime=row[28] #row[28] is the first_lift_up timestamp
            block=row[2]
            trial=row[3]
            offset=best_match_start(stime,offset)
            begin=offset #the begin index of the split data
            offset=best_match_end(etime,offset+1)#the next scan should begin at the last_matched_index add 1
            end=offset #the end index of the split data
            split_and_write(begin,end,block,trial,pid,headers2)

process()

