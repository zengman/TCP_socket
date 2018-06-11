#!/usr/bin/python  
#coding=utf-8 

import linecache
import json
from collections import OrderedDict

def readO(filename):
    dO = OrderedDict()
    with open(filename,'r') as f:
        temp1 = linecache.getline(filename, 11)
        temp1 = temp1.strip('\n')
        temp1 = temp1.strip()
        
        dO['APPROX_POSITION_XYZ'] = OrderedDict()             # 取基准站的坐标
        dO['APPROX_POSITION_XYZ']['x'] = temp1.split()[0]
        dO['APPROX_POSITION_XYZ']['y'] = temp1.split()[1]
        dO['APPROX_POSITION_XYZ']['z'] = temp1.split()[2]
        print("基站坐标")
        print(temp1.split()[0],temp1.split()[1],temp1.split()[2])
        
        array = []
        dO['Pseudorange'] = array                             # 取伪距
        for n in range(20, len(f.readlines())):
            temp2 = linecache.getline(filename, n)
            temp2 = temp2.strip('\n')
            temp2 = temp2.strip()
            d1 = OrderedDict()
            if(temp2.__contains__("> 2018 ")):
                d1['time'] = temp2[2:29]
                count = int(temp2.split()[8])
                d1['count'] = count
                for m in range(n + 1, n + count + 1):
                    temp3 = linecache.getline(filename, m)
                    temp3 = temp3.strip('\n')
                    temp3 = temp3.strip()
                    string = temp3[0:3]                      # 取卫星编号
                    satelliteNumber = string.replace(' ','') 
                    d1[satelliteNumber] = temp3[5:17]        # 取伪距
            else:
                continue
            array.append(d1)  
                 
    f.close()
    return dO
    # jsonstrO = json.dumps(dO)                
    # print(jsonstrO) 

# readO('3.obs')
