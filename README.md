#Snappy

Snappy is a command-line utility for taking and viewing photos with recent Sony cameras using the company's [SDK](http://camera.developer.sony.com). The full list of compatible cameras can be found [here], but the app has only been tested with the QX10.

##Install

Just clone the source into a convenient location. Be sure to check the list of dependencies for additional tools needed to run the app.

##Use

After you've connected to the camera as a wireless access point (no Bluetooth) you can just type the following into an open terminal:

`python snappy.py`

After the initial handshake takes place you'll be able to take photos by typing `snap` from the command-line prompt. Photos will automatically open in your default web browser.

##Status

The lack of documentation or even intelligible error messages stopped the project a lot earlier than I would have liked. I'm no longer actively working on it, but I'm holding out hope that future versions of the SDK will be better.