#!/usr/bin/python

import socket, sys, requests, cmd, readline, json
from bs4 import BeautifulSoup

#The parameters are important -- UDP, not TCP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

MAX = 65535
PORT = 1900

class snappyPrompt(cmd.Cmd):

	#defining attributes
	url = ''
	services = []
	ns_error = '*** Not supported by this camera'
	camera_str = 'camera'

	intro = 'Welcome to Snappy. Proceed when you\'re connected to your camera.'
	def do_snap(self, input_string):
		if (self.camera_str not in self.services):
			print self.ns_error
		else:
			target_url = ''.join([self.url, '/', self.camera_str])
			print target_url
			command_dict = {'method': 'actTakePicture', 'params': [], 'id': 1, 'version': '1.0'}
			command_json = json.dumps(command_dict)
			r = requests.post(target_url, command_json)
			print r.content

	def do_viewstream(self, input_string):
		print 'Starting the livestream'
	def do_printurl(self, input_string):
		#when referring to attributes, need to preface with self (OOP)
		print self.url
	def do_printservices(self, input_string):
		#same here
		for i in self.services:
			print i


def get_description():
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
	return requests.get('http://10.0.0.1:64321/DmsRmtDesc.xml')


#Gets the action list URL from the XML the camera provides
def GetURL(xml):

	#The search string needs to be lower case
	alu = xml.find('av:x_scalarwebapi_actionlist_url')
	if alu:
		print alu
		return alu.text
	else:
		raise Exception('The camera isn\'t supplying a URL')

#Gets the list of services available from the XML the camera provides
def GetServices(xml):
	services = xml.find_all('av:x_scalarwebapi_servicetype')
	if services:
		return services



def main():

	description = get_description()
	xml = BeautifulSoup(description.content)

	#Getting theActionListURL --- Need this to send commands to the camera
	actionListURL = GetURL(xml)
	#Need these too
	services = [i.text for i in GetServices(xml)]

	if actionListURL != None	and services != None:
		prompt = snappyPrompt()
		prompt.url = actionListURL
		prompt.services = services
		prompt.cmdloop()

	# presentUserChoices()

	if description is None:
		print 'Couldn\t get doc'



if __name__ == '__main__':
  main()