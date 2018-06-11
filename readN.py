#!/usr/bin/python  
#coding=utf-8 

import linecache
import json
from collections import OrderedDict
import timeCon

def readN(filename):
    dN = OrderedDict()
    with open(filename,'r') as f:
        for i in range(0, int((len(f.readlines())-5)/8)):
            for n in range(6 + i * 8, 12 + i * 8):
                temp = linecache.getline(filename, n)
                temp = temp.strip()
                temp = temp.strip('\n')
                
                if n % 8 == 6:
                    string = temp[0:3]
                    satelliteNumber = string.replace(' ','')
                    dN[satelliteNumber] = OrderedDict()             # 卫星编号
                    string_time = temp[4:23]
                    week, seconds = timeCon.GPS_to_GPSWeekSecond(string_time)
                    dN[satelliteNumber]['week'] = week
                    dN[satelliteNumber]['seconds'] = seconds        # GPS周和周内秒
                    a0 = temp[24:].split()[0]
                    dN[satelliteNumber]['a0'] = a0                  # 卫星时钟偏差（秒）
                    a1 = temp[24:].split()[1]
                    dN[satelliteNumber]['a1'] = a1                  # 卫星时钟漂移（秒/秒）
                    a2 = temp[24:].split()[2]
                    dN[satelliteNumber]['a2'] = a2                  # 卫星时钟漂移率（秒/秒的平方）
                    continue             
                
                elif n % 8 == 7:
                    AODE = temp.split()[0]
                    dN[satelliteNumber]['AODE'] = AODE              # 星历表数据有效龄期（N）
                    Crs = temp.split()[1]
                    dN[satelliteNumber]['Crs'] = Crs                # 轨道半径的正弦调和项改正的振幅（米）
                    delta_n = temp.split()[2]
                    dN[satelliteNumber]['delta_n'] = delta_n        # 由精密星历计算得到的卫星平均角速度与给定参数计算所得的平均角速度之差（弧度）
                    M0 = temp.split()[3]
                    dN[satelliteNumber]['M0'] = M0                  # 按参考历元toe计算的平近点角（弧度）
                    continue
                
                elif n % 8 == 0:
                    Cuc = temp.split()[0]            
                    dN[satelliteNumber]['Cuc'] = Cuc                # 升交距角的余弦调和项改正的振幅（弧度）
                    e = temp.split()[1]
                    dN[satelliteNumber]['e'] = e                    # 轨道偏心率
                    Cus = temp.split()[2]
                    dN[satelliteNumber]['Cus'] = Cus                # 升交距角的正弦调和项改正的振幅（弧度）
                    squareRoot_A = temp.split()[3]
                    dN[satelliteNumber]['squareRoot_A'] = squareRoot_A  # 轨道长半径的平方根（0.5mm)
                    continue
                
                elif n % 8 == 1:
                    toe = temp.split()[0]
                    dN[satelliteNumber]['toe'] = toe                # 星历表参考历元（秒）
                    Cic = temp.split()[1]
                    dN[satelliteNumber]['Cic'] = Cic                # 轨道倾角的余弦调和项改正的振幅（弧度）
                    OMEGA = temp.split()[2]
                    dN[satelliteNumber]['OMEGA'] = OMEGA            # 按参考历元toe计算的升交点赤经（弧度）
                    Cis= temp.split()[3]
                    dN[satelliteNumber]['Cis'] = Cis                # 轨道倾角的正弦调和项改正的振幅（弧度）
                    continue
                
                elif n % 8 == 2:
                    i = temp.split()[0]
                    dN[satelliteNumber]['i'] = i                    # 按参考历元toe计算的轨道倾角（弧度）
                    Crc = temp.split()[1]
                    dN[satelliteNumber]['Crc'] = Crc                # 轨道半径的余弦调和项改正的振幅（米）
                    omega = temp.split()[2]
                    dN[satelliteNumber]['omega'] = omega            # 近地点角距（弧度）
                    OMEGA_dot= temp.split()[3]
                    dN[satelliteNumber]['OMEGA_dot'] = OMEGA_dot    # 升交点赤经变化率（弧度/秒）
                    continue
                
                elif n % 8 == 3:
                    i_dot = temp.split()[0]
                    dN[satelliteNumber]['i_dot'] = i_dot            # 轨道倾角变化率（弧度/秒）
                    continue

    f.close()       
    # print(dN)   
    # print(dN['G7']['delta_n'])
    # print(dN['G7']['squareRoot_A'])  
    # print(dN['G7']['toe'])
    # print(dN['G7']['M0'])
    # print(dN['G7']['e'])
    # print(dN['G7']['omega'])
    # print(dN['G7']['Cuc'])
    # print(dN['G7']['Cus'])
    # print(dN['G7']['Crc'])
    # print(dN['G7']['Crs'])
    # print(dN['G7']['Cic'])
    # print(dN['G7']['Cis'])
    # print(dN['G7']['i_dot'])
    # print(dN['G7']['i'])
    # print(dN['G7']['OMEGA_dot'])
    # print(dN['G7']['OMEGA'])
    
         
    return dN
    

readN('3.nav')
