#!/usr/bin/python3

###############################################################
# Skript von Jan Metzing
# Kontakt: janmetzing@gmx.de
###############################################################
import datetime
import math
import RPi.GPIO as GPIO

class TriggerService:
    _gewAbstand = float
    _timeLastBang = datetime.datetime
    _startTime = datetime.datetime
    _vMeanSinceLastBang = []

    def __init__(self,GuiService,GpsImportService):
        self.GuiService = GuiService
        self.GpsImportService = GpsImportService
        self._startTime = datetime.datetime.now()
        self._timeLastBang = datetime.datetime.now() - self._startTime
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(3, GPIO.OUT)
        GPIO.output(3, False)
        self._gewAbstand = self.GuiService.getDesiredDistance()

    def go(self):
        self.trigger(self.GpsImportService.getVelocity())
        
    def trigger(self,vMeanNew):
        vGes = 0.0
        self._vMeanSinceLastBang.append(vMeanNew)
        for element in self._vMeanSinceLastBang:
            vGes += element
        vMean = vGes / len(self._vMeanSinceLastBang)
        vergleich = datetime.datetime.now()-self._startTime
        dTime = self.getTimeDiff(self._timeLastBang,vergleich)
        GPIO.output(3, False)
        if (dTime*vMean) >= self._gewAbstand:
            self.giveSignal()
            self._timeLastBang = datetime.datetime.now() -self._startTime
            del self._vMeanSinceLastBang[:]

    def giveSignal(self):
        GPIO.output(3, True)

    def getTimeDiff(self,time1,time2):
        if time1 >= time2:
            dt = time1 - time2
        else:
            dt = time2 - time1
        dtSec = dt.days*24*60*60 + dt.seconds + dt.microseconds/1000000
        return dtSec
