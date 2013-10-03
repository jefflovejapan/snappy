#!/usr/bin/python

import requests
import cmd
import json
import os
from bs4 import BeautifulSoup


class SnappyPrompt(cmd.Cmd):
    #defining attributes so I can reference them from main
    url = ''
    services = []
    ns_error = '*** Not supported by this camera'
    camera_str = 'camera'

    intro = 'Welcome to Snappy. Let\'s take some pictures!'

    def do_snap(self, input_string):
        if (self.camera_str not in self.services):
            print self.ns_error
        else:
            target_url = ''.join([self.url, '/', self.camera_str])
            command_dict = {'method': 'actTakePicture', 'params': [],
                            'id': 1, 'version': '1.0'}
            command_json = json.dumps(command_dict)
            r = requests.post(target_url, command_json)

            #loads the json string into a python dictionary
            response_dict = json.loads(r.text)
            image_url = str(response_dict.get('result')[0][0])
            open_result(image_url)

    def do_timer(self, input_string):
        if (self.camera_str not in self.services):
            print self.ns_error
        else:
            target_url = ''.join([self.url, '/', self.camera_str])
            command_dict = {'method': 'getSupportedSelfTimer', 'params': [],
                            'id': 1, 'version': '1.0'}
            command_json = json.dumps(command_dict)
            r = requests.post(target_url, command_json)
            response_dict = json.loads(r.text)
            timer_choices = str(response_dict.get('result')[0])

            while True:
                s = raw_input(' '.join(['How many seconds? ',
                                        str(timer_choices), ' ']))
                if s in timer_choices:
                    break

            #Camera throws a fit here -- "Illegal JSON". Sony's
            #documentation woefully incomplete.
            command_dict = {'method': 'setSelfTimer', 'params': [int(s)],
                            'id': 1, 'version': '1.0'}
            command_json = json.dumps(command_dict)
            print command_json
            r = requests.post(target_url, command_dict)
            print r.text

    def do_liveview(self, input_string):
        if (self.camera_str not in self.services):
            print self.ns_error
        else:
            target_url = ''.join([self.url, '/', self.camera_str])
            command_dict = {'method': 'startLiveview', 'params': [],
                            'id': 1, 'version': '1.0'}
            command_json = json.dumps(command_dict)
            r = requests.post(target_url, command_json)

            #loads the json string into a python dictionary
            response_dict = json.loads(r.text)
            stream_url = str(response_dict.get('result')[0])

            #unfinished implementation -- need to turn this streaming
            #data into jpegs (video?)
            r = requests.get(stream_url, stream=True)
            for line in r.iter_lines():
                if line:
                    print line


def open_result(url_string):
    os.system(' '.join(['open', url_string]))


def get_description():
    return requests.get('http://10.0.0.1:64321/DmsRmtDesc.xml')


#Gets the action list URL from the XML the camera provides
def get_url(xml):

    #The search string needs to be lower case
    alu = xml.find('av:x_scalarwebapi_actionlist_url')
    if alu:
        return alu.text
    else:
        raise Exception('The camera isn\'t supplying a URL')


#Gets the list of services available from the XML the camera provides
def get_services(xml):
    services = xml.find_all('av:x_scalarwebapi_servicetype')
    if services:
        return services


def main():

    description = get_description()
    xml = BeautifulSoup(description.content)

    #Getting theActionListURL --- Need this to send commands to the camera
    action_list_url = get_url(xml)
    #Need these too
    services = [i.text for i in get_services(xml)]

    if action_list_url is not None and services is not None:
        prompt = SnappyPrompt()
        prompt.url = action_list_url
        prompt.services = services
        prompt.cmdloop()

    if description is None:
        print 'Couldn\t get doc'

if __name__ == '__main__':
    main()
