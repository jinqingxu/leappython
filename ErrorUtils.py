# translate from android java code
# calculate all kinds of errors
import math

class ErrorUtils:
    liftUpX=0
    liftUpY=0
    touchDownX=0
    touchDownY=0
    targetWidth=0
    targetX=0
    targetY=0
    error=0
    SlipError=NarrowSlipError=ModerateSlipError=LargeSlipError=VeryLargeSlipError=0
    MissError=NearMissError=NotSoNearMissError=OtherError=AccidentalTap=0
    AccidentalHit=0

    def __init__(self,liftUpX,liftUpY,touchDownX,touchDownY,targetWidth,targetX,targetY):
        self.liftUpX=liftUpX
        self.liftUpY=liftUpY
        self.touchDownX=touchDownX
        self.touchDownY=touchDownY
        self.targetWidth=targetWidth
        self.targetX=targetX
        self.targetY=targetY

    # calculate the distance of two points in 2D-cors
    def distance(self,x1, y1, x2, y2):
        return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

    def calculateErrors(self):
        # if LiftUpX and LiftUpY inside the target, then it is not an Error
        # Set all the error = 0
        if self.isSelectionInsideTarget(self.liftUpX,self.liftUpY):
            self.error=0
            self.SlipError = self.NarrowSlipError = self.ModerateSlipError = self.LargeSlipError = self.VeryLargeSlipError = 0
            self.MissError = self.NearMissError = self.NotSoNearMissError = self.OtherError = self.AccidentalTap = 0
        # Otherwise, it is an Error
        # Determine if the Error is a Slip Error or a Miss Error
        else:
            self.error=1
            # Determine if the Error is a Slip Error
            # If TouchDown inside the target, then it is a Slip Error
            if self.isSelectionInsideTarget(self.touchDownX,self.touchDownY):
                self.SlipError=1
                # Determine the Sub-Category of the Slip Error
                if self.isSelectionInsideTarget2(self.liftUpX,self.liftUpY,0.5,0.75): # judge if left up position is within the range of 0.5 to 0.75
                    self.NarrowSlipError=1
                elif self.isSelectionInsideTarget2(self.liftUpX,self.liftUpY,0.75,1):
                    self.ModerateSlipError=1
                elif self.isSelectionInsideTarget2(self.liftUpX,self.liftUpY,1,1.5):
                    self.LargeSlipError=1
                else:
                    self.VeryLargeSlipError=1
            # If TouchDown is NOT inside the target, then it is a Miss Error
            else:
                self.MissError=1
                #  Determine the Sub-Category of the Miss Error
                if self.isSelectionInsideTarget2(self.liftUpX,self.liftUpY,0.5,0.75):
                    self.NearMissError=1
                elif self.isSelectionInsideTarget2(self.liftUpX,self.liftUpY,0.75,1):
                    self.NotSoNearMissError=1
                elif self.isSelectionInsideTarget2(self.liftUpX,self.liftUpY,1,1.5):
                    self.OtherError=1
                else:
                    self.AccidentalTap=1

        #  When touch down is far away, but it succeed, we call it an accidental hit
        if not(self.isSelectionInsideTarget(self.touchDownX,self.touchDownY)) and self.isSelectionInsideTarget(self.liftUpX,self.liftUpY):
            self.AccidentalHit=1




    # judge whether the touch point is inside the target
    def isSelectionInsideTarget(self,curX, curY):
        if self.distance(curX, curY, self.targetX, self.targetY) <= self.targetWidth * 0.5:
            return True
        else:
            return False

    # a is the bottom percentage b is the upper percentage
    def isSelectionInsideTarget2(self,curX,curY,a, b):
        if self.distance(curX,curY, self.targetX, self.targetY) > self.targetWidth * a \
                and self.distance(curX,curY, self.targetX,self.targetY) <= self.targetWidth * b:
            return True
        return False

