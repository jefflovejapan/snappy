#!/usr/bin/python

import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

MAX = 65535
PORT = 1900

def main():
	if sys.argv[1:] == ['client']:
		print 'Address before sending', s.getsockname()
	
		# Next step is to modify the "This is my message" bit, I think.
		# Need to build payload. Here's Sony's code:
	
		message = ('M-SEARCH * HTTP/1.1\r\n' +
		'HOST: 239.255.255.250:1900\r\n' +
		'MAN: "ssdp:discover"\r\n' +
		'MX: 10\r\n' +
		'ST: urn:schemas-sony-com:service:ScalarWebAPI:1\r\n' +
		'USER-AGENT: snappy.py\r\n\r\n')
	
		s.sendto(message, ('239.255.255.250', PORT))
		print 'Address after sending', s.getsockname()
		data, address = s.recvfrom(MAX) # overly promiscuous!
		print 'The server', address, 'says', repr(data)
	
	else:
		print >>sys.stderr, 'usage: udp_local.py server|client'


if __name__ == '__main__':
  main()