import socket
from contextlib import closing

class socket_array(object):
	def __init__(self,*ports):
		
		self.buffsize = 2**16
		self.sockets = {}
		
		for port in ports:
			
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect(('localhost',port))
			self.sockets[port] = s
			
	def __enter__(self):
		return self
		
	def __exit__(self,*args):
		for port in self.sockets:
			self.sockets[port].close()
	
	def display(self):
		
		for port in self.sockets:
			
			print " ***** %i ***** " % (port)
			rsp = self.sockets[port].recv(self.buffsize)
			print rsp
			
with socket_array(45481,45482,45484) as s:
	
	while True:
		
		cmd = raw_input("GCP> ")
		s.sockets[45481].send(cmd)
		s.display()
		
