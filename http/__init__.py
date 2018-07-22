import socket
import http.parser as parser
from threading import Thread
class WebServer:
	def __init__(self, port):
		self.port = port
		self.running = True
	def connection_handler(self, handler):
		self.handler = handler
	
	def init(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind(('', self.port))
	def acceptor(self, conn, addr):
		print("Yo")
		data = conn.recv(65565)
		try:
			data = data.decode('utf-8')
			data = parser.FormatHttpRequest(data)
		except KeyError:
			conn.send(
			#parser.httpPreparse("Not Found", "<center><h1>Bad request</h1></center>", code=403).encode("utf-8")
			b"HTTP/1.1 200 OK\r\nContent-Type: text/html;\r\n\r\n<center><h1>Bad Request</h1></center>"
			)
			return False
	#	print(data)
		datas=self.handler(conn,addr,data)
		conn.send(datas)
		conn.close()
	def start(self, maxConnection=False):
		if maxConnection:
			self.sock.listen(maxConnection)
		else:
			self.sock.listen()
		while self.running:
			self.connection, self.address = self.sock.accept()
			Thread(target=self.acceptor, args=(self.connection,self.address,)).start()
		self.sock.close()
			
			