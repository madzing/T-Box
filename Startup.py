#!/usr/bin/python3
from GpsImportService import GpsImportService
from Triggerservice import TriggerService
from GuiService import GuiService
import time
from ReadSerial import ReadSerial

### To let the GUI get ready
time.sleep(4)
###

gui = GuiService()
while True:
    if gui.getIsTrigger():
        serialRead = ReadSerial(gui.getPort(),gui.getBaudRate(),"$GPGGA.log","$GPRMC.log","w")
        serialRead.setDaemon(True)
        serialRead.start()
        importer = GpsImportService(gui)
        trigger = TriggerService(gui,importer)

        while gui.getIsTrigger():
            runTime = time.time()
            ####################################################
            importer.go()
            trigger.go()
            ####################################################
            endTime = time.time()
            wait = round((1/gui.getRunsPerSecond())-(endTime-runTime),5)
            if wait > 0:
                time.sleep(wait)
        serialRead.stop()
        serialRead.join()
    time.sleep(0.05)

