# append the twoDFitt file
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
firstTRE=[]
TRE=[]
# first error,then measurements from mackenzie,then measurements from Huang
def writeErrorForEveryTrial(pid,datas,headers):
    androidfile=path+'PID_'+str(pid)+'_TwoDFittsData_External.csv'
    with open(androidfile) as f:
        f_csv = csv.reader(f)
        for i in range(0, 9):  # skip the beginning
            next(f_csv)
        oldheaders=next(f_csv)
        # since first TRE and TRE are from Mackenzie,we need to move them behind
        headers=oldheaders # store the original header
        headers=headers[0:len(headers)-2]
        errorheaders=['Error','SlipError','NarrowSlipError','ModerateSlipError','LargeSlipError','VeryLargeSlipError','MissError','NearMissError','NotSoNearMissError','OtherError','AccidentalTap','AccidentalHit'] # the headers for the error data
        headers.extend(errorheaders)
        for row in f_csv:
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
            errorUtils.calculateErrors()
            errordata=[errorUtils.error,errorUtils.SlipError,errorUtils.NarrowSlipError,errorUtils.ModerateSlipError,errorUtils.LargeSlipError,errorUtils.VeryLargeSlipError,errorUtils.MissError,errorUtils.NearMissError,errorUtils.NotSoNearMissError,errorUtils.OtherError,errorUtils.AccidentalTap,errorUtils.AccidentalHit]
            row.extend(errordata)
            datas.append(row)
    return datas,headers


def writeMackenzieMeasurements(pid,files,datas,headers):
    macHeaders = ['FirstRe-Entry', 'AverageNumOfRe-Entry', 'MovementDirectionChangeX', 'MovementDirectionChangeY',
                 'MovementDirectionChangeZ', 'MovementOffset', 'MovementError', 'MovementVaribility']
    headers.extend(macHeaders)
    for i in range(len(files)):
        keys = files[i].split('_')
        block = keys[3]
        trial = int(keys[5][0:-4])
        leap = LeapAnalyzerMackenzie(path2 + files[i],pid,block,trial)
        leap.loadLeapData()
        leap.calculateNumberOfFrame()
        leap.calculateMovementDirectionChange()
        leap.calculateMovementOffset()
        leap.calculateMovementVariability(leap.movementOffset)
        leap.calculateMovementError()
        datas[i].append(firstTRE[i])
        datas[i].append(TRE[i])
        macData = [leap.movementDirectionChangeX, leap.movementDirectionChangeY, leap.movementDirectionChangeZ,
                   leap.movementOffset, leap.movementError, leap.movementVaribility]
        datas[i].extend(macData)
    return datas,headers

def writeHwangMeasurements(pid,files,datas,headers):
    hwangHeaders=['NumberOfPause','MeanPauseDuration(ms)','Verification Time(ms)','NumberOfSubmovement','PeekSpeed(mm/s)','NumberOfDecisionMaking','MeanDecisionMakingDuration(ms)']
    headers.extend(hwangHeaders)
    for i in range(len(files)):
        keys = files[i].split('_')
        block = keys[3]
        trial = int(keys[5][0:-4])
        leap = LeapAnalyzerHuang(path2+files[i], pid, block, trial)
        leap.loadLeapData()
        leap.getSubmovements()
        leap.calculatePauseTime()
        if leap.pauseTime!=0:
            t=0
        hwangData=[leap.pauseTime,leap.meanPauseDuration,leap.getVerificatonTime(),leap.getTotalNumOfSubMovement(),leap.trialPeekSpeed]
        leap2=LeapAnalyzerOriginal(path2+files[i],pid,block,trial)
        leap2.loadLeapData()
        leap2.calculateDecisionMakingDuration()
        hwangData.append(leap2.decisionMakingTime)
        hwangData.append(leap2.meanDecideMakingDuration)
        datas[i].extend(hwangData)
    return datas,headers


def writeFiles():
    # first write the error
    pid=848
    # the whole data list consists of the original data,error,measurement from Mackenzie and measurement form Huang
    # a two-dimentional array
    datas = []
    # the headers consists of the original headers,the error headers,mackenzie headers,hwang headers
    headers = []
    datas,headers=writeErrorForEveryTrial(pid,datas,headers)
    files = getSortedSplitFile(path2, pid)  # the files are sorted as the sequence of datas
    datas,headers=writeMackenzieMeasurements(pid,files,datas,headers)
    datas,headers=writeHwangMeasurements(pid,files,datas,headers)
    newfile = path + 'PID_' + str(pid) + '_TwoDFittsData_External_Measurements.csv'
    with open(newfile, 'w') as f:
        w_csv = csv.writer(f)
        w_csv.writerow(headers)
        for d in datas:
            w_csv.writerow(d)

writeFiles()