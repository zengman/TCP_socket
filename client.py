import socket #导入socket库
import json
#create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #32位地址，16位端口号，采用TCP连接
# build a connection
s.connect(('10.128.201.105',8888))
# print(s.recv(1024).decode('utf-8')) #接受1M内的数据解码后打印
s.send(b'request for data')
receive_str = s.recv(2048).decode('utf-8')
print(json.loads(receive_str))
# for data in [b'Michael',b'Tracy',b'Sarah']:
# 	s.send(data)
# 	print(s.recv(1024).decode('utf-8'))
s.send(b'exit')
s.close() #关闭连接


