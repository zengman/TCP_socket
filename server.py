import socket
import threading
import time

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('127.0.0.1',9999))
s.listen(5) #最大连接数,监听端口
print('Waiting for connection...')

def tcplink(sock,addr):
	print('Accept new connection from %s:%s...' % addr)
	sock.send(b'Welcome!')
	while True:
		data =  sock.recv(1024) #接受数据
		time.sleep(1)
		if not data or data.decode('utf-8')=='exit': #if not x判断d是否为none
			break
		sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
		print('connection form %s:%s closed' % addr)
while True:
	#接受一个新连接
	sock,addr = s.accept()
	#创建新线程来处理TCP连接
	t = threading.Thread(target=tcplink,args=(sock,addr))
	t.start()