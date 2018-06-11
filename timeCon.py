#!/usr/bin/python  
#coding=utf-8 

import datetime
import math

def idiv(a, b):
    return math.floor( a / b )
def UTC_to_GPSWeekSecond(string):                               # UTC时间转GPS周和GPS周内秒
    string = string.strip('\n')
    string = string.strip()
    year = int(string.split()[0])
    if( year < 1900 ):
        year = year + 1900
    month = int(string.split()[1])
    day = int(string.split()[2])
    hours = int(string.split()[3])
    minutes = int(string.split()[4]) 
    seconds = float(string.split()[5]) + 18
    if seconds >= 60:
        seconds = seconds - 60
        minutes = minutes + 1
        if minutes >= 60:
            minutes = minutes - 60
            hours = hours + 1
            if hours >= 24:
                hours = hours - 24
                day = day + 1
    elapsed = ((( hours * 60 ) + minutes ) * 60 ) + seconds
    
    def getMdj(y, m, d):
        mdj = 367 * y \
        - idiv(7 * (idiv(m + 9, 12) + y), 4) \
        - idiv(3 * (idiv(idiv(m + 9, 12) + y - 1, 100) + 1), 4) \
        + idiv(275 * m, 9) \
        + d + 1721028 - 2400000
        return mdj                                                # 儒略日
    
    GpsDayCount = getMdj(year, month, day) - getMdj(1980, 1, 6)   # GPS周
    GpsWeekCount = int(idiv(GpsDayCount, 7))
    GpsDay = GpsDayCount % 7
    GpsSecond = int(( GpsDay * 86400 ) + elapsed)                 # GPS周内秒
    
    return GpsWeekCount, GpsSecond
    # print(GpsWeekCount, GpsSecond)
def local_to_GPSWeekSecond(string):                               # 当地时间转GPS周和GPS周内秒
    string = string.strip('\n')
    string = string.strip()
    year = int(string.split()[0])
    if( year < 1900 ):
        year = year + 1900
    month = int(string.split()[1])
    day = int(string.split()[2])
    hours = int(string.split()[3]) - 8
    if hours < 0:
        hours = hours + 24
        day = day - 1
    minutes = int(string.split()[4]) 
    seconds = float(string.split()[5]) + 18
    if seconds >= 60:
        seconds = seconds - 60
        minutes = minutes + 1
        if minutes >= 60:
            minutes = minutes - 60
            hours = hours + 1
            if hours >= 24:
                hours = hours - 24
                day = day + 1
    elapsed = ((( hours * 60 ) + minutes ) * 60 ) + seconds
    
    def getMdj(y, m, d):
        mdj = 367 * y \
        - idiv(7 * (idiv(m + 9, 12) + y), 4) \
        - idiv(3 * (idiv(idiv(m + 9, 12) + y - 1, 100) + 1), 4) \
        + idiv(275 * m, 9) \
        + d + 1721028 - 2400000
        return mdj                                                # 儒略日
    
    GpsDayCount = getMdj(year, month, day) - getMdj(1980, 1, 6)   # GPS周
    GpsWeekCount = int(idiv(GpsDayCount, 7))
    GpsDay = GpsDayCount % 7
    GpsSecond = int(( GpsDay * 86400 ) + elapsed)                 # GPS周内秒
    print(GpsSecond)
    return  GpsSecond
    # print(GpsWeekCount, GpsSecond)


def GPS_to_GPSWeekSecond(string):                                 # GPS时间转GPS周和GPS周内秒
    string = string.strip('\n')
    string = string.strip()
    year = int(string.split()[0])
    if(year < 1900):
        year = year + 1900
    month = int(string.split()[1])
    day = int(string.split()[2])
    hours = int(string.split()[3])
    minutes = int(string.split()[4])
    seconds = float(string.split()[5])
    elapsed = (((hours * 60) + minutes) * 60) + seconds
    
    def getMdj(y, m, d):
        mdj = 367 * y \
            - idiv(7 * (idiv(m + 9, 12) + y), 4) \
            - idiv(3 * (idiv(idiv(m + 9, 12) + y - 1, 100) + 1), 4) \
            + idiv(275 * m, 9) \
            + d + 1721028 - 2400000
        return mdj                                                
    
    GpsDayCount = getMdj(year, month, day) - getMdj(1980, 1, 6)    # 儒略日
    GpsWeekCount = int(idiv(GpsDayCount, 7))                       # GPS周
    GpsDay = GpsDayCount % 7
    GpsSecond = int((GpsDay * 86400) + elapsed)                    # GPS周内秒
    
    return GpsWeekCount, GpsSecond
    # print(GpsWeekCount, GpsSecond)


local_to_GPSWeekSecond('2018  6 4 10  00 00.0000000')
# GPS_to_GPSWeekSecond('2018  5 29  14 50 17.0000000')

