#!/usr/bin/python

def main():
	try:
		import requests
		print 'Imported requests'
	except:
		print 'Couldn\'t import requests'

if __name__ == '__main__':
  main()