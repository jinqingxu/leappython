# for helper functions of processing file
import os

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

# in the path directory, find all the file begin with PID_pid
# return them in a sorted list
def getSortedSplitFile(path,pid):
    files = os.listdir(path)
    files = files[1:len(files)] # remove the '_DS.store' file
    files = sorted(files, file_cmp)
    result=[]
    for file in files:
        keys = file.split('_')
        if str(pid) in keys:  # if the file begins with PID_xxx
            result.append(file)
    return result