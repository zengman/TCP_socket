import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
from urllib import request
import json
url = "http://192.168.31.107:8888"
f=request.urlopen(url) 
response=f.read() 
print('—–response——') 
# print(str(response)) 
response = json.loads(response)
# print(response)
x  = []
y = []
z = []
for i in range(4):
    x.append(response['G'+str(i+1)]['X'])
    y.append(response['G'+str(i+1)]['Y'])
    z.append(response['G'+str(i+1)]['Z'])

# print(f.geturl()) 
# print(f.getcode())

# data = np.random.randint(0, 255, size=[40, 40, 40])

# x, y, z = data[0], data[1], data[2]

ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
#  将数据点分成三部分画，在颜色上有区分度
ax.scatter(x[0], y[0] ,z[0], c='y')  # 绘制数据点
ax.scatter(x[1], y[1], z[1], c='r')
ax.scatter(x[2], y[2], z[2], c='g')
ax.scatter(x[3], y[3], z[3], c="b")
x=-2752512
y=5242880
z=2490368

ax.scatter(x, y, z, c="pink")
x,y,z=-2145642.8675121125, 4396522.5499851685, 4078704.6437071455
ax.scatter(x, y, z, c="red")

ax.set_zlabel('Z')  # 坐标轴
ax.set_ylabel('Y')
ax.set_xlabel('X')
plt.show()