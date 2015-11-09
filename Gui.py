#!/usr/bin/python3

###############################################################
# Skript by Jan Metzing
# Contact: janmetzing@gmx.de
###############################################################

import datetime
import threading
import time
import io
from tkinter import * 
import os

class Gui(Frame):
    def createWidgets(self):
        self.settings.pack()

        self.port = Label(self.settings,text ="Port")
        self.port.grid(row=0,column=0)
        self.entryPort= Entry(self.settings)
        self.entryPort.grid(row=0,column=1)
        self.entryPort.insert(END,self.readSettingsFile("Port"))

        self.baudRate = Label(self.settings,text ="Baudrate")
        self.baudRate.grid(row=1,column=0)
        self.entryBaudRate= Entry(self.settings)
        self.entryBaudRate.grid(row=1,column=1)
        self.entryBaudRate.insert(END,self.readSettingsFile("Baud"))

        self.desiredDistance = Label(self.settings,text ="Desired distance (m)")
        self.desiredDistance.grid(row=2,column=0)
        self.entryDisiredDistance= Entry(self.settings)
        self.entryDisiredDistance.grid(row=2,column=1)
        self.entryDisiredDistance.insert(END,self.readSettingsFile("Desiered Distance"))

        self.acceptableDeviation = Label(self.settings,text ="Acceptable Deviation")
        self.acceptableDeviation.grid(row=3,column=0)
        self.entryAcceptableDeviation= Entry(self.settings)
        self.entryAcceptableDeviation.grid(row=3,column=1)
        self.entryAcceptableDeviation.insert(END,self.readSettingsFile("Acceptable Deviation"))

        self.runsPerSecond = Label(self.settings,text ="Runs per second")
        self.runsPerSecond.grid(row=4,column=0)
        self.entryRunsPerSecond= Entry(self.settings)
        self.entryRunsPerSecond.grid(row=4,column=1)
        self.entryRunsPerSecond.insert(END,self.readSettingsFile("Runs per Second"))

        self.smoothMode = Label(self.settings,text ="Smoothmode:")
        self.smoothMode.grid(row=5,column=0)

        self.secList = IntVar()
        self.gprmc = IntVar()
        self.simple = IntVar()
        self.modeSecList = Checkbutton(self.settings, text ="SecList",variable=self.secList)
        self.modeSecList.grid(row=5, column =1)
        
        self.modeGprmc = Checkbutton(self.settings, text ="Gprmc",variable=self.gprmc)
        self.modeGprmc.grid(row=5, column =2)
        
        self.modeSimple = Checkbutton(self.settings, text ="Simple",variable=self.simple)
        self.modeSimple.grid(row=5, column =3)

        self.getCurrentMode()
                
        self.lenListRaw = Label(self.settings,text ="Length of raw list")
        self.lenListRaw.grid(row=6,column=0)
        self.entryLenListRaw= Entry(self.settings)
        self.entryLenListRaw.grid(row=6,column=1)
        self.entryLenListRaw.insert(END,self.readSettingsFile("Length of rawlist"))

        self.lenListSmooth = Label(self.settings,text ="Length of smooth list")
        self.lenListSmooth.grid(row=7,column=0)
        self.entryLenListSmooth = Entry(self.settings)
        self.entryLenListSmooth.grid(row=7,column=1)
        self.entryLenListSmooth.insert(END,self.readSettingsFile("Length of smoothlist"))

    def getCurrentMode(self):
        secList = self.readSettingsFile("SecList")
        gprmc   = self.readSettingsFile("Gprmc")
        simple  = self.readSettingsFile("Simple")

        if (secList==1):
            self.modeSecList.select()
            self.modeGprmc.deselect()
            self.modeSimple.deselect()
        elif (gprmc ==1):
            self.modeSecList.deselect()
            self.modeGprmc.select()
            self.modeSimple.deselect()
        elif (simple ==1):
            self.modeSecList.deselect()
            self.modeGprmc.deselect()
            self.modeSimple.select()
        else:
            self.modeSecList.deselect()
            self.modeGprmc.deselect()
            self.modeSimple.deselect()
            
        
    def changeTriggerMode(self):
        if(self.isTrigger):
            self.stop = Button(self.choose, text ="Stop!", fg ="red", command = self.stopTriggering)
            self.stop.pack()
        else:
            self.start = Button(self.choose,text="Start!",fg ="green",command = self.startTriggering)
            self.start.pack()

    def readSettingsFile(self,wert):
        settingsFile = open("Settings","r")
        file = settingsFile.read()
        fileList = file.split("\n")
        for element in fileList:
            if wert in element:
                x = element.split(":")
                if(wert=="Port"):
                    return x[1]
                if(wert=="Baud"):
                    return int(x[1])
                return float(x[1])
        return "0"

    def writeSettingsFile(self):
        settingsFile = open("Settings","w")
        settingsFile.write("Port:" + str(self.entryPort.get())+"\n")
        settingsFile.write("Baud:" + str(self.entryBaudRate.get())+"\n")
        settingsFile.write("Trigger:" + str(self.isTrigger)+"\n")
        settingsFile.write("Desiered Distance:" + self.entryDisiredDistance.get()+"\n")
        settingsFile.write("Acceptable Deviation:" + self.entryAcceptableDeviation.get()+"\n")
        settingsFile.write("Runs per Second:" + self.entryRunsPerSecond.get()+"\n")
        settingsFile.write("SecList:"+str(self.secList.get())+"\n")
        settingsFile.write("Gprmc:"+str(self.gprmc.get())+"\n")
        settingsFile.write("Simple:"+str(self.simple.get())+"\n")
        settingsFile.write("Length of rawlist:"+self.entryLenListRaw.get()+"\n")
        settingsFile.write("Length of smoothlist:"+self.entryLenListSmooth.get())
        settingsFile.close()

    def checkRequirements(self):
        try:
            test = float(self.entryDisiredDistance.get())
            test = float(self.entryAcceptableDeviation.get())
            test = float(self.entryRunsPerSecond.get())
            test = float(self.entryLenListRaw.get())
            test = float(self.entryLenListSmooth.get())
        except:
            return False
        if((self.secList.get()==1 or self.gprmc.get() == 1 or self.simple.get() == 1)
           and self.secList.get()+self.gprmc.get()+self.simple.get() == 1):
            return True
        return False

    def startTriggering(self):
        if(self.checkRequirements()):
            self.isTrigger = True
            self.start.destroy()
            self.changeTriggerMode()
            self.writeSettingsFile()
            
            self.entryPort.configure(state = "disabled")
            self.entryBaudRate.configure(state = "disabled")
            self.entryDisiredDistance.configure(state = "disabled")
            self.entryAcceptableDeviation.configure(state = "disabled")
            self.entryRunsPerSecond.configure(state = "disabled")
            self.modeSecList.configure(state = "disabled")
            self.modeGprmc.configure(state = "disabled")
            self.modeSimple.configure(state = "disabled")
            self.entryLenListRaw.configure(state = "disabled")
            self.entryLenListSmooth.configure(state = "disabled")

            
        else:
            print("##############################################################")
            print("Please check your input! One or more requirements are not met!")
            print("##############################################################")
            

    def stopTriggering(self):
        self.isTrigger = False
        self.stop.destroy()
        self.changeTriggerMode()
        self.writeSettingsFile()
        self.entryPort.configure(state = "normal")
        self.entryBaudRate.configure(state = "normal")
        self.entryDisiredDistance.configure(state = "normal")
        self.entryAcceptableDeviation.configure(state = "normal")
        self.entryRunsPerSecond.configure(state = "normal")
        self.modeSecList.configure(state = "normal")
        self.modeGprmc.configure(state = "normal")
        self.modeSimple.configure(state = "normal")
        self.entryLenListRaw.configure(state = "normal")
        self.entryLenListSmooth.configure(state = "normal")

    def __init__(self, master = None):
        self.settings = Frame()
        self.settings.pack()
        self.choose = Frame()
        self.choose.pack()
        self.isTrigger = False
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.changeTriggerMode()
        self.writeSettingsFile()
        
        

################################################################################
root = Tk()
root.title("T-BOX")
app = Gui(master=root)
app.mainloop()
#root.destroy()
