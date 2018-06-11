#!/usr/bin/python
#coding=utf-8

from __future__ import division
import readN
import math
from collections import OrderedDict
import json

def satellite_coordinates_algorithm(t1, squareRootA, deltaN, Toc, Toe, a_0, a_1, a_2, m0, E, omega_w, cuc, cus, crc, crs, cic, cis, I, I_dot, OMEGA_w, OMEGA_dot_w):
    u = 3.986005 * 1e14                                          # 卫星坐标的算法
    We = 7.29211567 * 1e-5
    PI = 3.1415926
    n0 = u ** ( 1 / 2 ) / squareRootA ** 3
    n =  n0 + deltaN                                                   # 卫星运行的平均角速度n
    delta_t = a_0 + a_1 * ( t1 - Toc ) + a_2 * ( ( t1 - Toc ) ** 2 )
    t = t1 - delta_t
    tk = t - Toe
    
    if tk > 302400:
        tk = tk - 604800
    elif tk < -302400:
        tk = tk + 604800
    else:
        tk = tk                                                        # 归化时间tk
    
    mk = m0 + n * tk                                                   # 观测时刻卫星的平近角mk
    Ek0 = mk
    Ek = mk + E * math.sin( Ek0 )
    # Ek = mk + E * math.sin( Ek )
    while ( abs( Ek - Ek0 ) >= 1e-8 ):
        Ek0 = Ek
        Ek = mk + E * math.sin( Ek0 ) 

    cos_fk = ( math.cos(Ek) - E ) / ( 1 - E * math.cos(Ek) )
    sin_fk = math.sqrt( 1 - E ** 2 ) * math.sin(Ek) / ( 1 - E * math.cos(Ek) )
    if sin_fk > 0 and cos_fk > 0:
        fk = math.atan2( sin_fk , cos_fk)
    elif sin_fk > 0 and cos_fk < 0:
        fk = math.acos(cos_fk)
    elif sin_fk < 0 and cos_fk < 0:
        fk = PI - math.asin(sin_fk)
    else:
        fk = 2 * PI - math.acos(cos_fk)                                # 采用迭代算法计算偏近点角Ek
    # fk = math.atan( ( ( 1 - E ** 2 ) ** ( 1 / 2 ) ) * math.sin( Ek ) / ( math.cos( Ek ) - E ) )       # 真近点角fk
    Fk = fk + omega_w                                                 # 升交距角
    du = cuc * math.cos( 2 * Fk ) + cus * math.sin( 2 * Fk )
    dr = crc * math.cos( 2 * Fk ) + crs * math.sin( 2 * Fk )
    di = cic * math.cos( 2 * Fk ) + cis * math.sin( 2 * Fk )          # 摄动改正数
    uk = Fk + du                                                      # 经摄动改正后的升交距角uk
    rk = squareRootA ** 2 * ( 1 - E * math.cos( Ek ) ) + dr           # 经摄动改正后的卫星矢径rk
    ik = I + di + I_dot * tk                                          # 经摄动改正后的轨道倾角ik
    xk = rk * math.cos( uk )
    yk = rk * math.sin( uk )                                          # 卫星在轨道平面坐标系中的坐标
    OMEGA_K = OMEGA_w + ( OMEGA_dot_w - We ) * tk - We * Toe          # 观测时刻升交点经度OMEGA_K
    
    Xk = xk * math.cos( OMEGA_K ) - yk * math.cos( ik ) * math.sin( OMEGA_K )
    Yk = xk * math.sin( OMEGA_K ) + yk * math.cos( ik ) * math.cos( OMEGA_K )
    Zk = yk * math.sin( ik )                                          # 卫星在地固坐标系中的空间直角坐标
    
    return Xk, Yk, Zk

def getSatelliteCoordinates(t_weekSeconds):                           # 将计算卫星坐标所需的参数代入算法
    d = OrderedDict()
    satellite_parameters = readN.readN('3.nav')
    
    for x in range(0, len(satellite_parameters)):                        # 计算每颗卫星的坐标
        satellite_number = list(satellite_parameters.keys())[x]              
        d[satellite_number] = OrderedDict()                           # 将卫星编号作为每颗卫星的唯一标识
        toc = float(satellite_parameters[satellite_number]['seconds'])
        a0 = float(satellite_parameters[satellite_number]['a0'])
        a1 = float(satellite_parameters[satellite_number]['a1'])
        a2 = float(satellite_parameters[satellite_number]['a2'])
        Crs = float(satellite_parameters[satellite_number]['Crs'])
        delta_n = float(satellite_parameters[satellite_number]['delta_n'])
        M0 = float(satellite_parameters[satellite_number]['M0'])
        Cuc = float(satellite_parameters[satellite_number]['Cuc'])
        e = float(satellite_parameters[satellite_number]['e'])
        Cus = float(satellite_parameters[satellite_number]['Cus'])
        squareRoot_A = float(satellite_parameters[satellite_number]['squareRoot_A'])
        toe = float(satellite_parameters[satellite_number]['toe'])
        Cic = float(satellite_parameters[satellite_number]['Cic'])
        OMEGA = float(satellite_parameters[satellite_number]['OMEGA'])
        Cis = float(satellite_parameters[satellite_number]['Cis'])
        i = float(satellite_parameters[satellite_number]['i'])
        Crc = float(satellite_parameters[satellite_number]['Crc'])
        omega = float(satellite_parameters[satellite_number]['omega'])
        OMEGA_dot = float(satellite_parameters[satellite_number]['OMEGA_dot'])
        i_dot = float(satellite_parameters[satellite_number]['i_dot'])

        d[satellite_number]['x'], d[satellite_number]['y'], d[satellite_number]['z'] = \
        satellite_coordinates_algorithm(t_weekSeconds, squareRoot_A, delta_n, toc, toe, a0, a1, a2, M0, e, omega, Cuc, Cus, Crc, Crs, Cic, Cis, i, i_dot, OMEGA, OMEGA_dot)

    return d
    # jsonstrN = json.dumps(d)
    # print(jsonstrN)

# getSatelliteCoordinates(122318)