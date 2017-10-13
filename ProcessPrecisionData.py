# this script is replaced bt java and not used anymore
# this script is used for helping find the accurate position of start button

import csv
from GlobalVariables import *
from CalculateOfCircle import get_min_max_mean_deviation_from_list
from FileUtils import *

# get the range of x,y and z
def processPrecisionData(pid):

    file1 = pathHeaderForPrecision + 'PID_' + str(pid) + '/' + 'PID_' + str(pid) + '_Precision_Experiment_Timestamp.csv'
    timestamp_list = []

    # read leap data
    with open(file1) as f:

        f_csv = csv.reader(f)
        next(f_csv)  # skip the header
        for row in f_csv:
            timestamp_list.append(float(row[0])) # touch down timestamp
            timestamp_list.append(float(row[1])) # lift up timestamp

    file2 = pathHeaderForPrecision + 'PID_' + str(pid) + '/' + 'PID_' + str(pid) + '_Data_from_LEAPtest_results_Frame.csv'

    x_list = []
    y_list = []
    z_list = []

    # read leap data
    with open(file2) as f:

        f_csv = csv.reader(f)
        for i in range(0, 5):  # skip the beginning
            next(f_csv)

        for row in f_csv:

            # the first experiment of getting the average of y and z
            # timestamp_list[0] means the touch down timestamp when finger moves horizontally
            # timestamp_list[1] means the lift up timestamp when finger moves horizontally
            if float(row[2]) >= timestamp_list[0] and float(row[2]) < timestamp_list[1]:
                y_list.append(float(row[colNumLeapY]))
                z_list.append(float(row[colNumLeapZ]))

            # the second experiment of getting the average x
            # timestamp_list[2] means the touch down timestamp when finger moves vertically
            # timestamp_list[3] means the lift up timestamp when finger moves vertically
            if float(row[2]) >= timestamp_list[2] and float(row[2]) < timestamp_list[3]:
                x_list.append(float(row[colNumLeapX]))

    minX, maxX, averageX, deviationX = get_min_max_mean_deviation_from_list(x_list)
    minY, maxY, averageY, deviationY = get_min_max_mean_deviation_from_list(y_list)
    minZ, maxZ, averageZ, deviationZ = get_min_max_mean_deviation_from_list(z_list)

    writefile = pathHeaderForPrecision + 'Average_x_y_z_of_precision_experiment.csv'
    if not os.path.exists(writefile):
        with open(writefile, 'w') as f:
            w_csv = csv.writer(f)
            w_csv.writerow(['pid', 'averageX(mm)', 'averageY(mm)', 'averageZ(mm)','AbsDiffX(mm)','AbsDiffY(mm)','AbsDiffZ(mm)'])
            w_csv.writerow([pid,averageX, averageY, averageZ,abs(averageX-start3DX),abs(averageY-start3DY),abs(averageZ-start3DZ)])
    else:
        with open(writefile, 'a') as f:
            w_csv = csv.writer(f)
            w_csv.writerow([pid,averageX, averageY, averageZ,abs(averageX-start3DX),abs(averageY-start3DY),abs(averageZ-start3DZ)])

def process():
    # pid=raw_input("please enter pid: ")
    pids = getAllPids(pathHeaderForPrecision)
    writefile = pathHeaderForPrecision + 'Average_X_Y_Z_Of_Precision_Experiment.csv'
    if os.path.exists(writefile):
        os.remove(writefile)
    for p in pids:
        processPrecisionData(p)

process()
