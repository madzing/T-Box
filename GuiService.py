#!/usr/bin/python3

class GuiService():   
    def readSettingsFile(self,wert):
        settingsFile = open("Settings","r")
        file = settingsFile.read()
        fileList = file.split("\n")
        for element in fileList:
            if wert in element:
                x = element.split(":")
                return x[1]
    def getPort(self):
        try:
            self.port = self.readSettingsFile("Port")
            return self.port
        except:
            return self.port

    def getBaudRate(self):
        try:
            self.baudRate = self.readSettingsFile("Baud")
            return self.baudRate
        except:
            return self.baudRate
            
    def getIsTrigger(self):
        try:
            if self.readSettingsFile("Trigger") == "True":
                self.isTrigger = True
            else:
                self.isTrigger = False
            return self.isTrigger
        except:
            return self.isTrigger

    def getDesiredDistance(self):
        try:
            self.desieredDistance = float(self.readSettingsFile("Desiered Distance"))
            return self.desieredDistance
        except:
            return self.desieredDistance

    def getAcceptableDeviation(self):
        try:
            self.acceptableDeviation = float(self.readSettingsFile("Acceptable Deviation"))
            return self.acceptableDeviation
        except:
            return self.acceptableDeviation

    def getRunsPerSecond(self):
        try:
            self.runsPerSecond = float(self.readSettingsFile("Runs per Second"))
            return self.runsPerSecond
        except:
            return self.runsPerSecond 

    def getSmoothMode(self):
        try:
            if int(self.readSettingsFile("SecList"))==1:
                self.Smoothmode = "secList"
        
            elif int(self.readSettingsFile("Gprmc"))==1:
                self.Smoothmode = "GPRMC"
        
            elif int(self.readSettingsFile("Simple"))==1:
                self.Smoothmode = "simple"
            return self.Smoothmode
        except:
            return self.Smoothmode

    def getLogFile(self):
        try:
            if int(self.readSettingsFile("Gprmc"))==1:
                self.logFile = "$GPRMC.log"
        
            else:
                self.logFile = "$GPGGA.log"
            return self.logFile
        except:
            return self.logFile

    def getListDimensions(self):
        try:
            self.listDimensions = [int(self.readSettingsFile("Length of rawlist")),int(self.readSettingsFile("Length of smoothlist"))]
            return self.listDimensions
        except:
            return self.listDimensions

    def __init__(self):
        self.port = ""
        self.baudRate = 0
        self.isTrigger = False
        self.desieredDistance = 1.5
        self.acceptableDeviation = 1.0
        self.runsPerSecond = 50.0
        self.Smoothmode = "secList"
        self.logFile = "$GPGGA.log"
        self.listDimensions = [20,2]
        
