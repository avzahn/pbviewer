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
		
		self.socket.recv(self.buffsize)
		
	def __enter__(self):
		return self
		
	def __exit__(self,*args):
		self.socket.close()
		
	def __call__(self,msg):
		"""
		Dispatch a message to GCP and return the response contents
		"""
		try:
			self.socket.send(self.pack(msg))
			return self.unpack(self.socket.recv(self.buffsize))[1]
		except:
			print>>sys.stderr, "Connection failed; attempting reconnect"
			self.socket.close()
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.connect((self.host,self.port))
			
	def pack(self,msg):
		"""
		Form a GCP command packet with msg as the contents
		
		The format appears to be a 12 byte header followed by msg.
		The first two header bytes seem to be zero, followed by two
		bytes for the message length in bytes plus twelve, followed
		by six bytes of zeros, followed by two bytes the message
		length
		"""
		l=len(msg)
		return struct.pack('!6H%ic'%l,0,l+12,0,0,0,l,*list(msg))
		
	def unpack(self,rsp):
		"""
		Return a (header, contents) tuple from GCP responses
		
		The first 12 bytes of a response appear to be some sort
		of header that behaves similarly to the header expected
		from command messages. I haven't actually figured out
		how this response header works, but there seems to be
		little harm in ignoring it
		"""
		return rsp[0:12],rsp[12:]
		
if __name__ == "__main__":
	
	if len(sys.argv) == 1:
		host = 'localhost'
		port = 45481
	else:
		host = sys.argv[1]
		port = sys.argv[2]
	
	with ControlClient(host,port) as ctl:
		while True:
			print ctl(raw_input("GCP> "))

