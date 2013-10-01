#!/usr/bin/python

import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

MAX = 65535
PORT = 1900

if sys.argv[1:] == ['client']:
	print 'Address before sending', s.getsockname()

	# Next step is to modify the "This is my message" bit, I think.
	# Need to build payload. Here's Sony's code:

	# M-SEARCH * HTTP/1.1
	# HOST: 239.255.255.250:1900
	# MAN: "ssdp:discover"
	# MX: seconds to delay response (ex. MX: 1)
	# ST: urn:schemas-sony-com:service:ScalarWebAPI:1 USER-AGENT: OS/version product/version

	s.sendto('This is my message', ('239.255.255.250', PORT))
	print 'Address after sending', s.getsockname()
	data, address = s.recvfrom(MAX) # overly promiscuous!
	print 'The server', address, 'says', repr(data)

else:
	print >>sys.stderr, 'usage: udp_local.py server|client'


if __name__ == '__main__':
  main()