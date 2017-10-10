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

    # read leap data
    with open(file1) as f:

        f_csv = csv.reader(f)
        next(f_csv)  # skip the header
        for row in f_csv:
            timestamp_list.append(float(row[0]))
            timestamp_list.append(float(row[1]))

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

            if float(row[2]) >= timestamp_list[0]:

                x_list.append(float(row[colNumLeapX]))
                y_list.append(float(row[colNumLeapY]))
                z_list.append(float(row[colNumLeapZ]))
                break

    minX, maxX, averageX, deviationX = get_min_max_mean_deviation_from_list(x_list)
    minY, maxY, averageY, deviationY = get_min_max_mean_deviation_from_list(y_list)
    minZ, maxZ, averageZ, deviationZ = get_min_max_mean_deviation_from_list(z_list)

    writefile = pathHeaderForCrossHair + 'Average_X_Y_Z_Of_CrossHair_Experiment.csv'
    dateTimeLeap,dateTimeLeapStr=getDateTimeForLeapData(file2)
    if not os.path.exists(writefile):
        with open(writefile, 'w') as f:
            w_csv = csv.writer(f)
            w_csv.writerow(['pid', 'dateTime','averageX(mm)', 'averageY(mm)', 'averageZ(mm)','AbsDiffX(mm)','AbsDiffY(mm)','AbsDiffZ(mm)'])
            w_csv.writerow([float(pid),dateTimeLeapStr,averageX, averageY, averageZ,abs(averageX-start3DX),abs(averageY-start3DY),abs(averageZ-start3DZ)])
    else:



        with open(writefile, 'a') as f:

            w_csv = csv.writer(f)
            w_csv.writerow([float(pid),dateTimeLeapStr,averageX, averageY, averageZ,abs(averageX-start3DX),abs(averageY-start3DY),abs(averageZ-start3DZ)])



#pid=raw_input("please enter pid: ")
def process():
    '''

    maxPid = 0
    if  os.path.exists(writefile):

        with open(writefile, 'r') as f:
            f_csv = csv.reader(f)
            next(f_csv)  # get headers of csv

            for row in f_csv:
                if not row[0] == '':
                    if (float(row[0]) > maxPid):
                        maxPid = float(row[0])
    '''
    pids = getAllPids(pathHeaderForCrossHair)
    writefile = pathHeaderForCrossHair + 'Average_X_Y_Z_Of_CrossHair_Experiment.csv'
    if os.path.exists(writefile):
        os.remove(writefile)
    for p in pids:
        if  float(p)>=8897:
            processCrossHairData(p)
process()
