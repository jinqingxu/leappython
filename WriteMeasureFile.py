# append errors,measures from Mackenzie,measures from Hwang and measures of our work in the TwoD_measurement.csv file


from LeapAnalyzerMackenzie import *
from ErrorUtils import *
from FileUtils import *

from GlobalVariables import *
from Split import LeapTimeStamp

from FileUtils import  getSortedSplitFile

from LeapAnalyzerHwang import *
from LeapAnalyzerOriginal import LeapAnalyzerOriginal

# since TRE and firstTRE are calculated in the android code,we need to move them to the mackenzie measures part
# so use tmp variables to restore them
firstTRE=[]
TRE=[]

def loadLeapTimeStampData(path,pid):

    leapTimeStamp_list=[]

    leapTimeStampFile = path + 'PID_' + str(pid) + '_Leap_TimeStamp_Data.csv'

    with open(leapTimeStampFile) as f:

        f_csv=csv.reader(f)
        next(f_csv) # skip the header

        for row in f_csv:
            leapTimeStamp=LeapTimeStamp(row[0],row[1],row[2],row[3],row[4])
            leapTimeStamp_list.append(leapTimeStamp)

    os.remove(leapTimeStampFile)

    return leapTimeStamp_list

# restore the original data and append errors
def writeErrorForEveryTrial(pid,datas,pathFordata):

    androidfile=pathFordata+'PID_'+str(pid)+'_TwoDFittsData_External.csv'

    leapTimeStamp_list=loadLeapTimeStampData(pathFordata,pid)

    with open(androidfile) as f:

        f_csv = csv.reader(f)
        for i in range(0, 9):  # skip the beginning
            next(f_csv)
        oldheaders=next(f_csv) # get the old headers

        # since first TRE and TRE are from Mackenzie,we need to move them behind
        headers=oldheaders # store the original header
        headers=headers[0:len(headers)-2] # remove the 'firstTRE' and 'TRE'
        headers.extend(['leapStartTimestamp','leapFirstLiftUpTimeStamp','leapFinalLiftUpTimeStamp'])
        errorheaders=['Error','SlipError','NarrowSlipError','ModerateSlipError','LargeSlipError','VeryLargeSlipError','MissError','NearMissError','NotSoNearMissError','OtherError','AccidentalTap','AccidentalHit'] # the headers for the error data
        headers.extend(errorheaders) # append the error header to the headers
        i=0
        for row in f_csv:
            # restore the firstTRE and average TRE
            firstTRE.append(row[len(row)-2])
            TRE.append(row[len(row)-1])

            row = row[0:len(row) - 2] # omit the firstTRE and average TRE

            row.extend([leapTimeStamp_list[i].leapStartTimeStamp,leapTimeStamp_list[i].leapFirstLiftUpTimeStamp,leapTimeStamp_list[i].leapFinalLiftUpTime])


            targetX=float(row[colNumAndroidTargetX])
            targetY=float(row[colNumAndroidTargetY])
            firstTouchDownX=float(row[colNumAndroidFirstTouchDownX])
            firstTouchDownY=float(row[colNumAndroidFirstTouchDownY])
            firstLiftUpX=float(row[colNumAndroidFirstLiftUpX])
            firstLiftUpY=float(row[colNumAndroidFirstLiftUpY])
            targetWidthInPixel=float(row[colNumAndroidWidthInPixel])
            errorUtils=ErrorUtils(firstLiftUpX,firstLiftUpY,firstTouchDownX,firstTouchDownY,targetWidthInPixel,targetX,targetY)
            errorUtils.calculateErrors() # this function is used to calculate all kinds of errors,the results are the variables of ErrorUntils
            # restore the result in an array
            errordata=[errorUtils.error,errorUtils.SlipError,errorUtils.NarrowSlipError,errorUtils.ModerateSlipError,errorUtils.LargeSlipError,errorUtils.VeryLargeSlipError,errorUtils.MissError,errorUtils.NearMissError,errorUtils.NotSoNearMissError,errorUtils.OtherError,errorUtils.AccidentalTap,errorUtils.AccidentalHit]
            row.extend(errordata) # append the error data after the android data
            datas.append(row) # restore the data in a two-dimensional array

    return datas,headers



# append measures of mackenzie into datas and headers
def writeMackenzieMeasurements(pid,files,datas,headers,path,wrongIndex,wrong_list):

    # headers for measures from mackenzie
    macHeaders = ['FirstRe-Entry', 'AverageNumOfRe-Entry', 'MovementDirectionChangeX', 'MovementDirectionChangeY',
                 'MovementDirectionChangeZ', 'MovementOffset', 'MovementError', 'MovementVaribility','TaskAxisCrossing']
    headers.extend(macHeaders)

    for i in range(len(files)):
        # get the block and trial of current split file
        keys = files[i].split('_')
        block = keys[3]
        trial = int(keys[5][0:-4])

        leap = LeapAnalyzerMackenzie(path+'split/' + files[i],pid,block,trial,path)
        leap.loadLeapData()

        try:
            # leap.calculateNumberOfFrame()
            leap.calculateMovementDirectionChange()  # get the movement change on X,Y,Z axis

            leap.calculateMovementOffset()  # movement offset means the mean deviation from task plane based on the raw distance
            leap.calculateMovementVariability(
                leap.movementOffset)  # movement variability means the deviation from the average location
            leap.calculateMovementError()  # movement error means the deviation from task plane based on the absolute distance
            leap.calculateTaskPlaneCrossing()  # task axis crossing means passing through the task plane. we count how many times does it happend
            # since firstTRE and TRE belongs to the measures of Mackenzie,we append them as the begining of mackenzie data
            datas[i].append(firstTRE[i])
            datas[i].append(TRE[i])

            macData = [leap.movementDirectionChangeX, leap.movementDirectionChangeY, leap.movementDirectionChangeZ,
                       leap.movementOffset, leap.movementError, leap.movementVaribility, leap.taskAxisCrossing]

            # datas[i] means the current row of android data and error data
            datas[i].extend(macData)  # append mackenzie data

        except Exception as e:
            print "wrong pid,block,trial",leap.pid,leap.block,leap.trial
            wrongIndex.append(i)
            wrong_list.append([leap.pid,leap.block,leap.trial])
            continue


    return datas,headers,wrongIndex,wrong_list

# append measures of Hwang and our work into datas and headers
def writeHwangMeasurements(pid,files,datas,headers,path,wrongIndex,wrong_list):

    # headers for measures from Hwang
    hwangHeaders=['NumberOfDecisionMaking','MeanDecisionMakingDuration(ms)','Verification Time(ms)','NumberOfPause','MeanPauseDuration(ms)',
                  'PeekSpeed(mm/s)','NumberOfSubmovement']
    headers.extend(hwangHeaders)

    for i in range(len(files)):
        try:
            # get the current block and trial for the file
            keys = files[i].split('_')
            block = keys[3]
            trial = int(keys[5][0:-4])

            # measurements for HWang
            leap = LeapAnalyzerHwang(path + 'split/' + files[i], pid, block, trial, path)
            leap.loadLeapData()
            leap.getSubmovements()  # get the submovement_list,all measures from Hwang are based on this data
            leap.calculatePause()  # get how many pauses happens per trial and the mean pause duration
            leap.pid = pid

            # put data from measures of Hwang into an array
            hwangData = [leap.getVerificatonTime(), leap.pauseFrequency, leap.meanPauseDuration, leap.trialPeekSpeed,
                         leap.getTotalNumOfSubMovement()]

            # initial a Leap Analyzer for original measurments proposed in our work
            # there is current one measure called decisionMaking
            # decisionMaking means when the finger tip is very close to the tablet and within the area of 5/4 radius.
            # it serves as a supplement for verification time
            leap2 = LeapAnalyzerOriginal(path + 'split/' + files[i], pid, block, trial, path)
            leap2.loadLeapData()
            leap2.calculateDecisionMakingDuration()  # get how many time decision making happens and the mean duration
            originData = []
            originData.append(leap2.decisionMakingTime)  # append the data of decision making into the result array
            originData.append(leap2.meanDecideMakingDuration)

            # append datas from hwang and our work into the datas
            datas[i].extend(originData)
            datas[i].extend(hwangData)

        except Exception as e:
            print "wrong pid,block,trial", leap.pid,leap.block, leap.trial
            # how to remove data[i]?
            wrongIndex.append(i)
            wrong_list.append([leap.pid,leap.block, leap.trial])
            continue


    return datas,headers,wrongIndex,wrong_list


def writeFiles(pid,pathForResult,pathForData):
    # first write the error
    # the whole data list consists of the original data,error,measurement from Mackenzie and measurement form Huang
    # a two-dimentional array
    datas = []
    # the headers consists of the original headers,the error headers,mackenzie headers,hwang headers
    headers = []
    wrong_list=[]
    datas,headers=writeErrorForEveryTrial(pid,datas,pathForData) # append error datas ,those data only need data from android

    # the measurement from mackenzie,hwang and our work need the split data from leap motion
    files = getSortedSplitFile(pathForData+'split/')  # the files are sorted as the sequence of datas,block is of the highest priority,then trial
    wrongIndex=[]
    datas,headers,wrongIndex,wrong_list=writeMackenzieMeasurements(pid,files,datas,headers,pathForData,wrongIndex,wrong_list)  # append measures from Mackenzie
    datas,headers,wrongInde,wrong_list=writeHwangMeasurements(pid,files,datas,headers,pathForData,wrongIndex,wrong_list)   # append measures from Hwang

    # write the new TwoD_measurment file with all measurements
    # do not overwrite the old android data in case some problems occur. We need the raw data.
    newfile = pathForResult + 'PID_' + str(pid) + '_TwoDFittsData_External_Measurements.csv'

    with open(newfile, 'w') as f:
        w_csv = csv.writer(f)
        w_csv.writerow(headers)
        i=0
        for i in range(len(datas)):
            if i not in wrongIndex:
                w_csv.writerow(datas[i])

        writeWrongFile(wrong_list)



