import math
import numpy as np
import numpy.linalg as nlg
N = 0
def blh2xyz(B,L,H):

    dsm = 6378137
    df = 1/298.257223563
    # print(B)
    # print(L)
    # print(H)
    N = dsm/math.sqrt(1-df*(2-df)*math.sin(B)*math.sin(B))
    x = (N + H) * math.cos(B) * math.cos(L)
    y = (N + H) * math.cos(B) * math.sin(L)
    z = (N*(1-df*(2-df))+H)*math.sin(B)
    print(z)
    print("xyz:")
    print(x,y,z)
    # print(N)
    return x,y,z

def xyz2blh(x,y,z):
    dsm = 6378137
    df = 1/298.257223563
    R = math.sqrt(x*x + y*y)
    b0 = math.atan2(z,R)
    while True:
        N = dsm/math.sqrt(1.0-df*(2-df)*math.sin(b0)*math.sin(b0))
        b = math.atan2(z+N*df*(2-df)*math.sin(b0),R)
        if abs(b-b0)<1.0e-10:
            break
        b0 = b
    l = math.atan2(y,x)
    h = R/math.cos(b)-N
    return b,l,h

    # a = 6378136.49
    # b = 6356755.00
    # e_b = (a*a-b*b)/(b*b)
    # e_a = (a*a-b*b)/(a*a)
    # # print(math.pow(2,5))
    # th_t = math.sqrt(x*x + y*y) * b
    # theta = math.atan((z*a)/th_t)


    # L = math.atan(y/x)

    # ff = z + e_b * b * math.pow(math.sin(theta),3)
    # mm = math.sqrt(x*x+y*y) - e_a * a * math.pow(math.cos(theta), 3)
    # print("blh:")
    # B = ff/mm
    # kk = math.sqrt(1-e_a*math.sin(B)*math.sin(B))
    # N = a/kk
    # H = math.sqrt(x*x + y*y)/math.cos(B) - N
    # print(B,L,H)
    # print(N)
    # return B,L,H
def DMS_RAD(dms):
    M_PI = 3.1415926
    deg = int(dms)
    print(deg)
    Min = int((dms-deg)*100)
    print(Min)
    sec = ((dms - deg)*100 - Min)*100
    print(sec)
    rad = (deg + Min/60 + sec/3600)/180.0*M_PI
    print(rad)
    return rad

def rad_dms(rad):
    M_PI = 3.1415926
    ar = rad
    if rad < 0:
        ar = -rad
    ar += 10e-10
    ar = ar * 180/M_PI
    deg = int(ar)
    am = (ar-deg) * 60
    Min = int(am)
    sec = (am-Min)*60
    dms = deg + Min/100 + sec/10000.0
    if rad < 0:
        dms = - dms
    return dms

# b =(30*3600+31*60+40.23)/3600
# l = (114*3600+21*60+20.51)/3600

# b = DMS_RAD(b)
# print(b)
# l = DMS_RAD(l)
B = 39.962935
L = 116.354986
H = 40
L = DMS_RAD(L)
B = DMS_RAD(B)

# x,y,z = blh2xyz(B,L,H)
x,y,z=-2167516.3951, 4394219.4653 ,4069717.0123
x1=-2752512
x2=5242880
x3=2490368
# 98109233550885.70312500

# x,y,z =  -4334058.588358545 ,8146510.617066625 ,7714821.133730192 
b,l,h = xyz2blh(x1,x2,x3)
b = rad_dms(b)
l = rad_dms(l)
print("b,l,h")
print(b,l,h)
# x,y,z = blh2xyz(b,l,h)
# b,l,h = xyz2blh(x,y,z)
# x,y,z = blh2xyz(b,l,h)
# b,l,h = xyz2blh(x,y,z)


def fun1(b,l,h, dsmiaxis, dfla):
    b = DMS_RAD(b)
    l = DMS_RAD(l)
    

a = [[2.8294179287909243E7, 1.0056211423414357E7, 466304.77358201146, -1053564.5410568416 ],
              [-1.8493695959850714E7, 3765448.465063764, -292790.6057312973, 3323063.3023865 ],
              [-1.7255707067245435E7 ,-1.8650028447094582E7, -9214822.297116665, -4154145.823571481 ],
              [7455223.739186905 ,4828368.558616462, 9041308.129265951 ,1884647.0622418225 ]]
# a=a/1e6

a = np.array(a)
# print(a)
print("det:")
print(nlg.det(a))
a = nlg.inv(a)
# print(a)
# print(a[0][0])
b = [[-2.102427422255728E13],
              [6.787655173119234E13],
              [-7.843540750099428E13],
              [3.158312999235922E13]]
b = np.mat(b)
# print(a*b)

# c = [[3,6],[4,7]]
# c=np.mat(c)
# print(nlg.inv(c))
# print(np.multiply(a,b))

print(2**4*3)