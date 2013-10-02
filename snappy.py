#!/usr/bin/python

import socket, sys, requests, cmd, readline
from bs4 import BeautifulSoup

#The parameters are important -- UDP, not TCP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

MAX = 65535
PORT = 1900

class snappyPrompt(cmd.Cmd):
	intro = 'Welcome to Snappy. Proceed when you\'ve connected to your camera.'
	def do_snap():
		print 'took a photo: SNAP'


def GetURL(xml):

	#The search string needs to be lower case
	alu = xml.find('av:x_scalarwebapi_actionlist_url')
	if alu:
		print alu
		return alu.text
	else:
		raise Exception('The camera isn\'t supplying a URL')

def GetServices(xml):
	services = xml.find_all('av:x_scalarwebapi_servicetype')
	if services:
		return services



def main():

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
	description = requests.get('http://10.0.0.1:64321/DmsRmtDesc.xml')
	xml = BeautifulSoup(description.content)

	#Getting theActionListURL --- Need this to send commands to the camera
	actionListURL = GetURL(xml)
	print actionListURL
	services = GetServices(xml)
	for i in services:
		print i.text

	if actionListURL != None	and services != None:
		prompt = snappyPrompt()
		prompt.cmdloop()


	# presentUserChoices()

	if description is None:
		print 'Couldn\t get doc'



if __name__ == '__main__':
  main()