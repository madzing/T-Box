#!/usr/bin/python3

###############################################################
# Script written by Jan Metzing
# Kontakt: janmetzing@gmx.de
###############################################################

import math
import datetime

"""
Objects build by this class are meant to store and manage Gps-Data-Lists.
One element of said list has the following structure:
[b,time,pos]
b    -> boolean            -> Was the measurement refered to as reliable?
time -> datetime.timedelta -> timedifference to first measurement done this cruise
pos  -> [lat,lon]          -> Position
"""
class GpsList:
    def __init__(self,maxListLen,acceptableDeviation):
        self.__list = []
        self.__maxListLen = maxListLen
        self.__acceptableDeviation = acceptableDeviation

#### "Public Methods" ####
    """Adds a new element to the List. If the list has too many elements
       the oldest one will be deleted. Returns if the new Element was accepted.
       @param definitelyReliable, Boolean True-->definitely reliable, False-->reliability will be checked
       @param pos, [lat,lon] (float), Position
       @param time, datetime.timedelta, timedifference to first measurement done this cruise."""
    def writeNewPos(self,definitelyReliable,pos,time):
        if definitelyReliable == False:
            definitelyReliable = self.__isReliable(pos,time) #Test reliability
        self.__list.append([definitelyReliable,time,pos]) #append list
        if len(self.__list) > self.__maxListLen:
            self.__list.pop(0) #delete oldest measurement
        return definitelyReliable
    
    """Returns the mean velocity of accepted elements (m/s).
       @param smooth -> int : "case" 0: no smoothing (__vmeanStepByStep())
                              "case" 1: only first and last element are used (__vmeanFirstToLast())
                              "case" 2: (__vmeanStepByStep() + __vmeanFirstToLast()) / 2"""
    def getVmean(self,smooth):
        if smooth == 0:
            return round(self.__vmeanStepByStep(),5)
        elif smooth == 1:
            return round(self.__vmeanFirstToLast(),5)
        else:
            return round((self.__vmeanStepByStep() + self.__vmeanFirstToLast())/2,5)

    """Returns the mean Time of all accepted elements"""
    def getTimeMean(self):
        goodList = self.getGoodDataList()
        lenGoodList = len(goodList)
        time = datetime.timedelta()
        for i in range(lenGoodList):
            time += goodList[i][1]
        return time / lenGoodList

    """Returns the mean Position of all accepted elements"""
    def getPositionMean(self):
        goodList = self.getGoodDataList()
        lenGoodList = len(goodList)
        posx = 0.0
        posy = 0.0
        for i in range(lenGoodList):
            posx += goodList[i][2][0]
            posy += goodList[i][2][1]
        return [posx/lenGoodList,posy/lenGoodList]

    """Returns a list that only includes accepted measurements"""
    def getGoodDataList(self):
        goodDataList = []
        for i in range(len(self.__list)):
            if self.__list[i][0]:
                goodDataList.append(self.__list[i])
        return goodDataList

#### "Private Methods" ####
    """Returns True if a new measurement is considered reliable otherwise False will be returned."""
    def __isReliable(self,pos,time):
        goodList = self.getGoodDataList()
        lenGoodList = len(goodList)
        if lenGoodList<=self.__maxListLen/2:
            return True
        else:
            vNew = self.__distanceCalc(pos,goodList[lenGoodList-1][2])/self.__getTimeDiff(time,goodList[lenGoodList-1][1])
            vMean = self.__vmeanStepByStep()
            if vNew > vMean + vMean*self.__acceptableDeviation or vNew < vMean -vMean*self.__acceptableDeviation:
                return False
            else:
                return True

    """Returns the distance between two Positions (m)."""
    def __distanceCalc(self,pos1,pos2):
        start_lat = math.radians(pos1[0])
        start_long = math.radians(pos1[1])
        end_lat = math.radians(pos2[0])
        end_long = math.radians(pos2[1])
        d_lat = end_lat - start_lat
        d_long = end_long - start_long
        a = math.sin(d_lat/2)**2 + math.cos(start_lat) * math.cos(end_lat) * math.sin(d_long/2)**2
        c = 2 * math.atan2(math.sqrt(a),  math.sqrt(1-a))
        return 6371 * c *1000

    """Returns the time difference between two times (datetime.timedelta) in seconds."""
    def __getTimeDiff(self,time1,time2):
        if time1 >= time2:
            dt = time1 - time2
        else:
            dt = time2 - time1
        dtSec = dt.days*24*60*60 + dt.seconds + dt.microseconds/1000000
        return dtSec

    """Returns vmean (m/s), all accepted elements are used."""
    def __vmeanStepByStep(self):
        goodList = self.getGoodDataList()
        distance = 0.0
        for i in range(len(goodList)-1):
            distance += self.__distanceCalc(goodList[i][2],goodList[i+1][2])
        time = self.__getTimeDiff(goodList[0][1],goodList[len(goodList)-1][1])
        return distance / time

    """Returns vmean (m/s), only the first and last accepted element is used."""
    def __vmeanFirstToLast(self):
        goodList = self.getGoodDataList()
        distance = self.__distanceCalc(goodList[0][2],goodList[len(goodList)-1][2])
        time = self.__getTimeDiff(goodList[0][1],goodList[len(goodList)-1][1])
        return distance / time
