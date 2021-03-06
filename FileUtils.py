# for helper functions of processing file
import os
import csv
import time
from GlobalVariables import *
# compare the filename by block then trial
def file_cmp(x,y):
    key1=x.split('_')
    key2=y.split('_')
    block1=int(key1[3])
    block2=int(key2[3])
    trial1=int(key1[5][0:-4])
    trial2=int(key2[5][0:-4])
    if block1<block2: # the highest priority is block
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
'''
# not used any more
# in the path directory, find all the split file
# return them in a sorted list
def getSortedSplitFile(path,pid):
    files = os.listdir(path)
    files = sorted(files, file_cmp)
    result=[]
    for file in files:
        keys = file.split('_')
        if str(pid) in keys:  # if the file begins with PID_xxx
            result.append(file)
    return result
'''

# in the path directory, find all the split file
# return them in a sorted list
def getSortedSplitFile(path):
    files = os.listdir(path)
    files = sorted(files, file_cmp)
    result=[]
    for file in files:
        result.append(file)
    return result


# get all pid in a folder
def getAllPids(path):

    pid_list=[]
    for dir in os.listdir(path):
        child = os.path.join(path, dir)
        if os.path.isdir(child):
            keys = child.split('/')
            if keys[len(keys) - 1][0:4] == 'PID_':  # go through all the folder that contain datas from experiment
                keys2 = keys[len(keys) - 1].split('_')  # split PID_pid to get the pid
                pid = keys2[len(keys2) - 1]
                pid_list.append(pid)

    return pid_list

def writeWrongFile(wrong_list):
    if len(wrong_list)<1:
        return
    file=""
    pid=wrong_list[0][0]
    if float(pid)<200:
        file=pathHeaderForData+'Old Adults/'+'PID_'+str(pid)+'/'+'wrongTrial_PID'+str(pid)+'_file.csv'
    else:
        file = pathHeaderForData + 'Young Adults/' + 'PID_' + str(pid) + '/' +'wrongTrial_PID_'+str(pid)+'_file.csv'

    if os.path.exists(file):
        with open(file, 'a') as f:
            f_csv = csv.writer(f)

            for row in wrong_list:
                f_csv.writerow(row)
    else:
        with open(file, 'w') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(['pid', 'block', 'trial'])
            for row in wrong_list:
                f_csv.writerow(row)
    f.close()

