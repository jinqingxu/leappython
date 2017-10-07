# this script is replaced bt java and not used anymore
# this script is used for helping find the accurate position of start button

import csv
from GlobalVariables import *
from CalculateOfCircle import get_min_max_mean_deviation_from_list

def setStartPosition(pid):

    #xBoundary = 5  # the abs(x) should be less than 5, or it's an error frame
    file1 = pathHeaderForCrossHair + 'PID_' + str(pid) + '/' + 'PID_'+str(pid)+'_Data_from_LEAPtest_results_Frame.csv'
    headers = []  # for headers of the csv file
    x_list = []
    y_list = []
    z_list = []
    warmpUpTimeStamp = float(raw_input("please enter the warm up timestamp: "))
    # read leap data
    with open(file1) as f:

        f_csv = csv.reader(f)
        for i in range(0, 5):  # skip the beginning
            next(f_csv)

        for row in f_csv:

            if float(row[2])>=warmpUpTimeStamp:
                x_list.append(float(row[colNumLeapX]))
                y_list.append(float(row[colNumLeapY]))
                z_list.append(float(row[colNumLeapZ]))

    minX,maxX,averageX,deviationX=get_min_max_mean_deviation_from_list(x_list)
    minY, maxY, averageY, deviationY = get_min_max_mean_deviation_from_list(y_list)
    minZ, maxZ, averageZ, deviationZ = get_min_max_mean_deviation_from_list(z_list)

    #print round(averageX,2),round(averageY,2),round(averageZ,2)
    print 'Y:',round(averageY,2)
    print 'Z:',round(averageZ,2)

pid=8888
setStartPosition(pid)
