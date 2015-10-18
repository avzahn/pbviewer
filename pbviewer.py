import socket
from contextlib import closing

with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
	s.connect(('localhost',45481))
	
	while True:
		
		cmd = raw_input("GCP>")
		s.send(cmd)
		rsp = s.recv(2048)
		print rsp
		
