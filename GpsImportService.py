#!/usr/bin/python3
from GpsList import GpsList
from ReadSerial import ReadSerial
from GpsRead import GpsRead
import datetime


class GpsImportService():

    def __init__(self,GuiService):
        self.smoothMode = GuiService.getSmoothMode()
        self.lenListRaw = GuiService.getListDimensions()[0]
        self.rawList = GpsList(self.lenListRaw,1)
        self.lenListSmooth = GuiService.getListDimensions()[1]
        self.smoothList = GpsList(self.lenListSmooth,0)
        self.gpsRead = GpsRead(GuiService.getLogFile())
        self.startTime = datetime.datetime.now()
        self.GPRMCvelocity = 0.0
        self.rawListLongEnough = False   
        self.velocity = 0
        self.isNewPos = False 

    def go(self):
        self.isNewPos = False 
        if self.gpsRead.istNewData():
            print(str(self.getVelocity())+" m/s")
            if self.smoothMode == "GPRMC":
                    try:
                        self.velocity = self.gpsRead.getNewData()
                    except:
                        print("$GPRMC input probably defective")
                        
            elif self.smoothMode == "simple":
                try:
                    self.isNewPos = self.rawList.writeNewPos(False,self.gpsRead.getNewData(),datetime.datetime.now()-self.startTime)
                    if not self.rawListLongEnough:
                        self.rawListLongEnough = len(self.rawList.getGoodDataList()) >= self.lenListRaw/2
                except:
                    print("$GPGGA input probably defective")
                if self.isNewPos and self.rawListLongEnough:
                    self.velocity = self.rawList.getVmean(2)
                    
            else:
                try:
                    self.isNewPos = self.rawList.writeNewPos(False,self.gpsRead.getNewData(),datetime.datetime.now()-self.startTime)
                    if not self.rawListLongEnough:
                        self.rawListLongEnough = len(self.rawList.getGoodDataList()) >= self.lenListRaw/2
                except:
                    print("$GPGGA input probably defective")
                if self.isNewPos and self.rawListLongEnough:
                    self.smoothList.writeNewPos(True,self.rawList.getPositionMean(),self.rawList.getTimeMean())
                    if len(self.smoothList.getGoodDataList()) == self.lenListSmooth:
                        self.velocity = self.smoothList.getVmean(1)
        
    def getVelocity(self):
        return self.velocity
