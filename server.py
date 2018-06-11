import socket
import threading
import time
import json

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('192.168.31.107',20000))
s.listen(5) #最大连接数,监听端口
print('Waiting for connection...')
dd = dict()
dd['test'] = 1
data2client={}
data2client["code"]=dd
data2client["id"]=1900
data2client["name"]='张三'
data2client["sex"]='男'
data2client["info"]='info'
data2client["data"]='list'

jsonStr = json.dumps(data2client)
print(jsonStr)


def tcplink(sock,addr):
	print('Accept new connection from %s:%s...' % addr)
	# sock.send(b'Welcome!')
	while True:
		data =  sock.recv(1024) #接受数据
		print("shu : "+str(data))
		time.sleep(1)
		if not data or data.decode('utf-8')=='exit': #if not x判断d是否为none
			break
		if data.decode('utf-8') == "request for data":
			print(data)
			sock.send(jsonStr.encode('utf-8'))
			print('send json')
		# sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
		print('connection form %s:%s closed' % addr)
while True:
	#接受一个新连接
	sock,addr = s.accept()
	#创建新线程来处理TCP连接
	t = threading.Thread(target=tcplink,args=(sock,addr))
	t.start()