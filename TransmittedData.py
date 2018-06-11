#!/usr/bin/python
#coding=utf-8

from __future__ import division
import getSatelliteCoordinates
import readO
from collections import OrderedDict
import timeCon
import json

def transmittedData(t_weekSeconds):
    d = OrderedDict()                                                           # 调整格式前的汇总信息
    d1 = OrderedDict()                                                          # 观测时间和前四颗卫星的伪距信息
                                                             # 通过计算前四颗卫星的坐标与基准站坐标得出的真实距离
    d4 = OrderedDict()                                                          # 调整格式后的汇总信息（包含伪距改正数，伪距改正数的变化率，卫星坐标和观测时间）
    d5 = OrderedDict()                                                          # 卫星在观测文件中最后一个时间段（即最新）时间的坐标
    d6 = OrderedDict()                                                          # 卫星在观测文件中从第一个时间段开始第一次遍历到该卫星时的时间的坐标

    temp = readO.readO('3.obs')                                                 # 从观测文件读取出的基准站坐标、观测时间和伪距信息
    APPROX_POSITION_X = float(temp['APPROX_POSITION_XYZ']['x'])                 # 基准站的坐标信息
    APPROX_POSITION_Y = float(temp['APPROX_POSITION_XYZ']['y'])
    APPROX_POSITION_Z = float(temp['APPROX_POSITION_XYZ']['z'])
    
    count = len(temp['Pseudorange']) - 1
    d1['Pseudorange'] = OrderedDict()
    string = temp['Pseudorange'][count]['time']                                 # 取观测文件中最后一个时间段（即最新）的时间
    GPSweek, GPSseconds = timeCon.GPS_to_GPSWeekSecond(string)
    d1['Pseudorange']['time'] = str(GPSweek) + " " + str(GPSseconds)
    
    flag = 0
    for i in range(1, len(temp['Pseudorange'][count])):                         # 取观测文件中最后一个时间段（即最新）的伪距信息
        # if flag >= temp['Pseudorange'][count]['count']:    
        if flag >= 6:                                                       # 取到四颗卫星的伪距信息即停止
            break
        cnkey = list(temp['Pseudorange'][count].keys())
        temp1 = cnkey[i]
        cnv = list(temp['Pseudorange'][count].values())
        d1['Pseudorange'][temp1] = cnv[i]
        flag = flag + 1
    
    d['satelliteCoordinates'] = OrderedDict()
    d2 = getSatelliteCoordinates.getSatelliteCoordinates(t_weekSeconds)         # 所有卫星当前时刻的坐标
    for i in range(1, len(d1['Pseudorange'])):
        for j in range(0, len(d2)):                       
            if list(d1['Pseudorange'].keys())[i] == list(d2.keys())[j]:
                string1 = list(d1['Pseudorange'].keys())[i]
                d['satelliteCoordinates'][string1] = OrderedDict()
                d['satelliteCoordinates'][string1]['X'] = d2[string1]['x']
                d['satelliteCoordinates'][string1]['Y'] = d2[string1]['y']
                d['satelliteCoordinates'][string1]['Z'] = d2[string1]['z']
                break
    
    # d3['realDistance'] = OrderedDict()
    # for i in range(0, len(d['satelliteCoordinates'])):                          # 计算取到的四颗卫星到基准站的真实距离
    #     string2 = list(d['satelliteCoordinates'].keys())[i]
    #     d3['realDistance'][string2] = (( float(d['satelliteCoordinates'][string2]['X']) - APPROX_POSITION_X ) ** 2 \
    #     + ( float(d['satelliteCoordinates'][string2]['Y']) - APPROX_POSITION_Y ) ** 2 \
    #     + ( float(d['satelliteCoordinates'][string2]['Z']) - APPROX_POSITION_Z ) ** 2 ) ** ( 1 / 2 )
    
    d['pseudorange_Corrections'] = OrderedDict()
    # d['pseudorange_Corrections']['time'] = d1['Pseudorange']['time']
    # for i in range(0, len(d3['realDistance'])):                                 # 计算取到的四颗卫星的伪距改正数
    #     string3 = list(d3['realDistance'].keys())[i]
    #     d['pseudorange_Corrections'][string3] = float(d3['realDistance'][string3]) - float(d1['Pseudorange'][string3])
    
    d['ratio_pseudorange_Corrections'] = OrderedDict()
    for i in range(1, len(d1['Pseudorange'])):                                  # 计算取到的四颗卫星的伪距改正数的变化率
        for j in range(0, len(temp['Pseudorange'])):
            flag1 = False
            for k in range(2, len(temp['Pseudorange'][j])):
                if list(d1['Pseudorange'].keys())[i] == list(temp['Pseudorange'][j].keys())[k]:        # 取在观测文件中从第一个时间段开始第一次遍历到该卫星时的伪距
                    string4 = list(d1['Pseudorange'].keys())[i]
                    string5 = list(temp['Pseudorange'][j].values())[0]
                    gps_week, gps_seconds = timeCon.GPS_to_GPSWeekSecond(string5)
                    
                    d5 = getSatelliteCoordinates.getSatelliteCoordinates(GPSseconds)       # 卫星在观测文件中最后一个时间段（即最新）时间的坐标
                    d6 = getSatelliteCoordinates.getSatelliteCoordinates(gps_seconds)      # 卫星在观测文件中从第一个时间段开始第一次遍历到该卫星时的时间的坐标
                    realDistance_GPSseconds = ((float(d5[string4]['x']) - APPROX_POSITION_X ) ** 2 \
                    + ( float(d5[string4]['y']) - APPROX_POSITION_Y ) ** 2 \
                    + ( float(d5[string4]['z']) - APPROX_POSITION_Z ) ** 2 ) ** ( 1 / 2 )     # 在观测文件中最后一个时间段（即最新）时间时卫星和观测站之间的真实距离
                    realDistance_gps_seconds = ((float(d6[string4]['x']) - APPROX_POSITION_X ) ** 2 \
                    + ( float(d6[string4]['y']) - APPROX_POSITION_Y ) ** 2 \
                    + ( float(d6[string4]['z']) - APPROX_POSITION_Z ) ** 2 ) ** ( 1 / 2 )     # 在观测文件中从第一个时间段开始第一次遍历到该卫星的时间时卫星和观测站之间的真实距离

                    d['pseudorange_Corrections'][string4] = realDistance_GPSseconds - float(d1['Pseudorange'][string4])

                    delta_seconds = GPSseconds - gps_seconds
                    delta_week = GPSweek - gps_week
                    if delta_seconds < 0:
                        delta_seconds = delta_seconds + 604800
                        delta_week = delta_week - 1
                    delta_t = delta_week * 604800 + delta_seconds

                    delta_pseudorange_Corrections = \
                    ( realDistance_GPSseconds - float(list(d1['Pseudorange'].values())[i]) ) \
                    - ( realDistance_gps_seconds - float(list(temp['Pseudorange'][j].values())[k]))   
                    if delta_t != 0:
                        d['ratio_pseudorange_Corrections'][string4] = delta_pseudorange_Corrections / delta_t
                    # else:
                    #     d['ratio_pseudorange_Corrections'][string4] = 0
                    flag1 = True
                    break   
            if flag1 == True:
                break

    for i in range(0, len(d['satelliteCoordinates'])):                       # 变换数据字典的格式
        string6 = list(d['satelliteCoordinates'].keys())[i]
        string = "G"+str(i+1)
        d4[string] = OrderedDict()
        d4[string]['pseudorange_Corrections'] = d['pseudorange_Corrections'][string6]
        d4[string]['ratio_pseudorange_Corrections'] = d['ratio_pseudorange_Corrections'][string6]
        d4[string]['X'] = d['satelliteCoordinates'][string6]['X']
        d4[string]['Y'] = d['satelliteCoordinates'][string6]['Y']
        d4[string]['Z'] = d['satelliteCoordinates'][string6]['Z']
        d4[string]['number'] = string6
    
    d4['time'] = d1['Pseudorange']['time']
    d4['cnt'] = len(d['satelliteCoordinates'])
    # print(json.dumps(d4)+'\n')
    return d4
    # print(json.dumps(temp)+'\n')
    # print(json.dumps(d)+'\n')
    # print(json.dumps(d1)+'\n')
    # print(json.dumps(d2)+'\n')
    # print(json.dumps(d3)+'\n')
    
    # print(json.dumps(d5)+'\n')
    # print(json.dumps(d6))
# transmittedData(317784)
