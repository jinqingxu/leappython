# this script is replaced bt java and not used anymore
# this script is used for helping find the accurate position of start button

import csv
from GlobalVariables import *
from CalculateOfCircle import get_min_max_mean_deviation_from_list
from FileUtils import *

# get the range of x,y and z
def processCrossHairData(pid):

    file1 = pathHeaderForCrossHair + 'PID_' + str(pid) + '/' + 'PID_' + str(pid) + '_CrossHair_Experiment_Timestamp.csv'
    timestamp_list = []

    # read the timestamp : touch down
    with open(file1) as f:

        f_csv = csv.reader(f)
        next(f_csv)  # skip the header
        for row in f_csv:
            timestamp_list.append(float(row[0]))


    file2 = pathHeaderForCrossHair + 'PID_' + str(pid) + '/' + 'PID_' + str(pid) + '_Data_from_LEAPtest_results_Frame.csv'

    x_list = []
    y_list = []
    z_list = []

    # read leap data
    with open(file2) as f:

        f_csv = csv.reader(f)
        for i in range(0, 5):  # skip the beginning
            next(f_csv)

        for row in f_csv:

            if float(row[2]) >= timestamp_list[0]: # timestamp_list[0] means the touch down timstamp and row[2] is the timestamp of a frame

                x_list.append(float(row[colNumLeapX]))
                y_list.append(float(row[colNumLeapY]))
                z_list.append(float(row[colNumLeapZ]))
                break

    minX, maxX, averageX, deviationX = get_min_max_mean_deviation_from_list(x_list)
    minY, maxY, averageY, deviationY = get_min_max_mean_deviation_from_list(y_list)
    minZ, maxZ, averageZ, deviationZ = get_min_max_mean_deviation_from_list(z_list)

    writefile = pathHeaderForCrossHair + 'Average_X_Y_Z_Of_CrossHair_Experiment.csv'
    dateTimeLeap,dateTimeLeapStr=getDateTimeForLeapData(file2) # get the dateTime of the leap motion data
    # a new result file
    if not os.path.exists(writefile):
        with open(writefile, 'w') as f:
            w_csv = csv.writer(f)
            w_csv.writerow(['pid', 'dateTime','averageX(mm)', 'averageY(mm)', 'averageZ(mm)','AbsDiffX(mm)','AbsDiffY(mm)','AbsDiffZ(mm)'])
            w_csv.writerow([float(pid),dateTimeLeapStr,averageX, averageY, averageZ,abs(averageX-start3DX),abs(averageY-start3DY),abs(averageZ-start3DZ)])
    else:
        # append
        with open(writefile, 'a') as f:

            w_csv = csv.writer(f)
            w_csv.writerow([float(pid),dateTimeLeapStr,averageX, averageY, averageZ,abs(averageX-start3DX),abs(averageY-start3DY),abs(averageZ-start3DZ)])



#pid=raw_input("please enter pid: ")

def process():
    pids = getAllPids(pathHeaderForCrossHair)
    writefile = pathHeaderForCrossHair + 'Average_X_Y_Z_Of_CrossHair_Experiment.csv'
    # remove the existing result file
    if os.path.exists(writefile):
        os.remove(writefile)
    # go through all the pid
    for p in pids:
        processCrossHairData(p)

process()
