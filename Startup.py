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
serialRead = ReadSerial("/dev/ttyUSB0",4800,"$GPGGA.log","$GPRMC.log","w")
serialRead.start()
while True:
    time1 = time.time()
    if gui.getIsTrigger():   
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
    time2 = time.time()
    sleep = round((((1/10)-(time2-time1))),5)
    if sleep > 0:
        time.sleep(sleep)
