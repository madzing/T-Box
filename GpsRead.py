#!/usr/bin/python3

###############################################################
# Script written by Jan Metzing
# Kontakt: janmetzing@gmx.de
###############################################################
import os

class GpsRead:
    _eingabe = ""
    _fin = os
    _letzteDatenmenge = 0

    def __init__(self,eingabe):
        self._eingabe = eingabe
        self._fin = open(eingabe)
        for line in self._fin:
           self._fin.readline()
        statinfo = os.stat(self._eingabe)
        self._letzteDatenmenge = statinfo.st_size

    def istNewData(self):
        statinfo = os.stat(self._eingabe)
        if self._letzteDatenmenge < statinfo.st_size:
            self._letzteDatenmenge = statinfo.st_size
            return True
        else:
            return False

    def getNewData(self):
        latString = ""
        lonString = ""
        string = self._fin.readline()
        if '$GPGGA' in string:
            startPos = self.findnth(string,',',2)
            trennzeichenPos = self.findnth(string,',',3)
            endPos = self.findnth(string,',',5)

            latString = string[startPos+1:trennzeichenPos]
            lonString = string[trennzeichenPos+3:endPos]
            return [float(latString)/100,float(lonString)/100]
        elif '$GPRMC' in string:
            startPos = self.findnth(string,',',7)
            endPos = self.findnth(string,',',8)
            velocity = string[startPos+1:endPos]
            return float(velocity)
            
    def findnth(self,s, substr, n):
        offset = -1
        for i in range(n):
            offset = s.find(substr, offset+1)
            if offset == -1: break
        return offset
