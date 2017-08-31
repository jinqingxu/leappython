# append errors,measures from Mackenzie,measures from Hwang and measures of our work in the TwoD_measurement.csv file

from GlobalVariables import path2 # the split path
from GlobalVariables import  path
from LeapAnalyzerMackenzie import *
from ErrorUtils import *

from GlobalVariables import offsetAndroidWidthInPixel
from GlobalVariables import offsetAndroidFirstLiftUpX
from GlobalVariables import offsetAndroidFirstLiftUpY
from GlobalVariables import offsetAndroidTargetX
from GlobalVariables import  offsetAndroidTargetY
from GlobalVariables import offsetAndroidFirstTouchDownX
from GlobalVariables import  offsetAndroidFirstTouchDownY

from FileUtils import  getSortedSplitFile

from LeapAnalyzerHuang import LeapAnalyzerHuang
from LeapAnalyzerOriginal import LeapAnalyzerOriginal

# since TRE and firstTRE are calculated in the android code,we need to move them to the mackenzie measures part
# so use tmp variables to restore them
firstTRE=[]
TRE=[]

# restore the original data and append errors
def writeErrorForEveryTrial(pid,datas,headers):

    androidfile=path+'PID_'+str(pid)+'_TwoDFittsData_External.csv'

    with open(androidfile) as f:
        f_csv = csv.reader(f)
        for i in range(0, 9):  # skip the beginning
            next(f_csv)
        oldheaders=next(f_csv) # get the old headers

        # since first TRE and TRE are from Mackenzie,we need to move them behind
        headers=oldheaders # store the original header
        headers=headers[0:len(headers)-2] # remove the 'firstTRE' and 'TRE'
        errorheaders=['Error','SlipError','NarrowSlipError','ModerateSlipError','LargeSlipError','VeryLargeSlipError','MissError','NearMissError','NotSoNearMissError','OtherError','AccidentalTap','AccidentalHit'] # the headers for the error data
        headers.extend(errorheaders) # append the error header to the headers

        for row in f_csv:
            # restore the firstTRE and TRE
            firstTRE.append(row[len(row)-2])
            TRE.append(row[len(row)-1])

            row = row[0:len(row) - 2]
            targetX=float(row[offsetAndroidTargetX])
            targetY=float(row[offsetAndroidTargetY])
            firstTouchDownX=float(row[offsetAndroidFirstTouchDownX])
            firstTouchDownY=float(row[offsetAndroidFirstTouchDownY])
            firstLiftUpX=float(row[offsetAndroidFirstLiftUpX])
            firstLiftUpY=float(row[offsetAndroidFirstLiftUpY])
            targetWidthInPixel=float(row[offsetAndroidWidthInPixel])
            errorUtils=ErrorUtils(firstLiftUpX,firstLiftUpY,firstTouchDownX,firstTouchDownY,targetWidthInPixel,targetX,targetY)
            errorUtils.calculateErrors() # this function is used to calculate all kinds of errors,the results are the variables of ErrorUntils
            # restore the result in an array
            errordata=[errorUtils.error,errorUtils.SlipError,errorUtils.NarrowSlipError,errorUtils.ModerateSlipError,errorUtils.LargeSlipError,errorUtils.VeryLargeSlipError,errorUtils.MissError,errorUtils.NearMissError,errorUtils.NotSoNearMissError,errorUtils.OtherError,errorUtils.AccidentalTap,errorUtils.AccidentalHit]
            row.extend(errordata) # append the error data after the android data
            datas.append(row) # restore the data in a two-dimensional array

    return datas,headers

# append measures of mackenzie into datas and headers
def writeMackenzieMeasurements(pid,files,datas,headers):

    # headers for measures from mackenzie
    macHeaders = ['FirstRe-Entry', 'AverageNumOfRe-Entry', 'MovementDirectionChangeX', 'MovementDirectionChangeY',
                 'MovementDirectionChangeZ', 'MovementOffset', 'MovementError', 'MovementVaribility','TaskAxisCrossing']
    headers.extend(macHeaders)

    for i in range(len(files)):
        # get the block and trial of current split file
        keys = files[i].split('_')
        block = keys[3]
        trial = int(keys[5][0:-4])

        leap = LeapAnalyzerMackenzie(path2 + files[i],pid,block,trial)
        leap.loadLeapData()
        # leap.calculateNumberOfFrame()
        leap.calculateMovementDirectionChange() # get the movement change on X,Y,Z axis
        leap.calculateMovementOffset() # movement offset means the mean deviation from task plane based on the raw distance
        leap.calculateMovementVariability(leap.movementOffset) # movement variability means the deviation from the average location
        leap.calculateMovementError() # movement error means the deviation from task plane based on the absolute distance
        leap.calculateTaskAxisCrossing() # task axis crossing means passing through the task plane. we count how many times does it happend
        # since firstTRE and TRE belongs to the measures of Mackenzie,we append them as the begining of mackenzie data
        datas[i].append(firstTRE[i])
        datas[i].append(TRE[i])

        macData = [leap.movementDirectionChangeX, leap.movementDirectionChangeY, leap.movementDirectionChangeZ,
                   leap.movementOffset, leap.movementError, leap.movementVaribility,leap.taskAxisCrossing]

        # datas[i] means the current row of android data and error data
        datas[i].extend(macData) # append mackenzie data

    return datas,headers

# append measures of Hwang and our work into datas and headers
def writeHwangMeasurements(pid,files,datas,headers):

    # headers for measures from Hwang
    hwangHeaders=['NumberOfPause','MeanPauseDuration(ms)','Verification Time(ms)','NumberOfSubmovement','PeekSpeed(mm/s)','NumberOfDecisionMaking','MeanDecisionMakingDuration(ms)']
    headers.extend(hwangHeaders)

    for i in range(len(files)):
        # get the current block and trial for the file
        keys = files[i].split('_')
        block = keys[3]
        trial = int(keys[5][0:-4])

        leap = LeapAnalyzerHuang(path2+files[i], pid, block, trial)
        leap.loadLeapData()
        leap.getSubmovements() # get the submovement_list,all measures from Hwang are based on this data
        leap.calculatePauseTime() # get how many pauses happens per trial and the mean pause duration
        # put data from measures of Hwang into an array
        hwangData=[leap.pauseTime,leap.meanPauseDuration,leap.getVerificatonTime(),leap.getTotalNumOfSubMovement(),leap.trialPeekSpeed]
        # initial a Leap Analyzer for measures of our work
        # there is current one measure called decision making
        # decision making means when the finger tip is very close to the tablet and within the area of 5/4 radius.
        leap2=LeapAnalyzerOriginal(path2+files[i],pid,block,trial)
        leap2.loadLeapData()
        leap2.calculateDecisionMakingDuration() # get how many time decision making happens and the mean duration
        hwangData.append(leap2.decisionMakingTime) # append the data of decision making into the result array
        hwangData.append(leap2.meanDecideMakingDuration)

        # append datas from hwang and our work into the datas
        datas[i].extend(hwangData)

    return datas,headers


def writeFiles():
    # first write the error
    pid=849
    # the whole data list consists of the original data,error,measurement from Mackenzie and measurement form Huang
    # a two-dimentional array
    datas = []
    # the headers consists of the original headers,the error headers,mackenzie headers,hwang headers
    headers = []

    datas,headers=writeErrorForEveryTrial(pid,datas,headers) # append error datas ,those data only need data from android

    # the measurement from mackenzie,hwang and our work need the split data from leap motion
    files = getSortedSplitFile(path2, pid)  # the files are sorted as the sequence of datas,block is of the highest priority,then trial
    datas,headers=writeMackenzieMeasurements(pid,files,datas,headers)  # append measures from Mackenzie
    datas,headers=writeHwangMeasurements(pid,files,datas,headers)   # append measures from Hwang
    # write the new TwoD_measurment file with all measurements
    # do not overwrite the old android data in case some problems occur. We need the raw data.
    newfile = path + 'PID_' + str(pid) + '_TwoDFittsData_External_Measurements.csv'
    with open(newfile, 'w') as f:
        w_csv = csv.writer(f)
        w_csv.writerow(headers)
        for d in datas:
            w_csv.writerow(d)


writeFiles()