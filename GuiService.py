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

            self.port = self.readSettingsFile("Port")
            return self.port

    def getBaudRate(self):
            self.baudRate = self.readSettingsFile("Baud")
            return self.baudRate

    def getIsTrigger(self):
            if self.readSettingsFile("Trigger") == "True":
                self.isTrigger = True
            else:
                self.isTrigger = False
            return self.isTrigger

    def getDesiredDistance(self):
            self.desieredDistance = float(self.readSettingsFile("Desiered Distance"))
            return self.desieredDistance

    def getAcceptableDeviation(self):
            self.acceptableDeviation = float(self.readSettingsFile("Acceptable Deviation"))
            return self.acceptableDeviation

    def getRunsPerSecond(self):
            self.runsPerSecond = float(self.readSettingsFile("Runs per Second"))
            return self.runsPerSecond

    def getSmoothMode(self):
            if int(self.readSettingsFile("SecList"))==1:
                self.Smoothmode = "secList"

            elif int(self.readSettingsFile("Gprmc"))==1:
                self.Smoothmode = "GPRMC"

            elif int(self.readSettingsFile("Simple"))==1:
                self.Smoothmode = "simple"
            return self.Smoothmode

    def getLogFile(self):
            if int(self.readSettingsFile("Gprmc"))==1:
                self.logFile = "$GPRMC.log"

            else:
                self.logFile = "$GPGGA.log"
            return self.logFile

    def getListDimensions(self):
            self.listDimensions = [float(self.readSettingsFile("Length of rawlist")),float(self.readSettingsFile("Length of smoothlist"))]
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
