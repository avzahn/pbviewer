#! /bin/python27
import socket
import struct
import sys

class ControlClient(object):
	
	def __init__(self,host,port):
		self.buffsize = 2**16
		self.host = host
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((host,port))
		print>>sys.stderr, self.socket.recv(self.buffsize)
		
	def __enter__(self):
		return self
		
	def __exit__(self,*args):
		self.socket.close()
		
	def __call__(self,msg):
		try:
			self.socket.send(self.pack(msg))
			return self.socket.recv(self.buffsize)
		except:
			print>>sys.stderr, "Connection failed; attempting reconnect"
			self.socket.close()
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.connect((self.host,self.port))
			
	def pack(self,msg):
		l=len(msg)
		return struct.pack('!6H%ic'%l,0,l+12,0,0,0,l,*list(msg))

with ControlClient('localhost',45481) as ctl:
	while True:
		print ctl(raw_input("GCP> "))

