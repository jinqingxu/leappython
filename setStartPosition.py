# this script is replaced bt java and not used anymore
# this script is used for helping find the accurate position of start button

import csv
from GlobalVariables import *
from CalculateOfCircle import get_min_max_mean_deviation_from_list

def setStartPosition(pid):

    xBoundary = 5  # the abs(x) should be less than 5, or it's an error frame
    file1 = pathheader + 'PID_' + str(pid) + '/' + 'Data from LEAPtest_results_PID_' + str(
        pid) + '_Frame.csv'  # leap data

    headers = []  # for headers of the csv file
    x_list = []
    y_list = []
    z_list = []
    # read leap data
    with open(file1) as f:

        f_csv = csv.reader(f)
        for i in range(0, 4):  # skip the beginning
            next(f_csv)
        headers = next(f_csv)  # get headers of csv
        headers2 = ['PID', 'Block', 'Trial', 'Amplitude(mm)', 'Width(mm)', 'Direction']
        headers2.extend(headers)  # headers2 is for the result file

        for row in f_csv:

            if abs(float(row[offsetLeapX]))<xBoundary:

                x_list.append(float(row[offsetLeapX]))
                y_list.append(float(row[offsetLeapY]))
                z_list.append(float(row[offsetLeapZ]))

    minX,maxX,averageX,deviationX=get_min_max_mean_deviation_from_list(x_list)
    minY, maxY, averageY, deviationY = get_min_max_mean_deviation_from_list(y_list)
    minZ, maxZ, averageZ, deviationZ = get_min_max_mean_deviation_from_list(z_list)

    print round(averageX,2),round(averageY,2),round(averageZ,2)

pid=8888
setStartPosition(pid)
