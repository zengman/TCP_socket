import socket #导入socket库
#create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #32位地址，16位端口号，采用TCP连接
# build a connection
s.connect(('127.0.0.1',9999))
print(s.recv(1024).decode('utf-8')) #接受1M内的数据解码后打印
for data in [b'Michael',b'Tracy',b'Sarah']:
	s.send(data)
	print(s.recv(1024).decode('utf-8'))
s.send(b'exit')
s.close() #关闭连接

