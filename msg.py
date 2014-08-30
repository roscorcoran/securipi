#!/usr/bin/python
import io
import time
import base64
import picamera
import requests
import json
import RPi.GPIO as GPIO 

#Callback
def takeapic():
	with picamera.PiCamera() as camera:
		camera.vflip = True
		camera.hflip= True
		camera.led = True
		camera.capture('image.jpg')
		#Camera.led = False
		camera.close()
		print 'Closed Cam'
	files = {'file': open('image.jpg', 'r+b')}
	#files = {'file': ('image', open('image.jpg', 'r+b'), 'image/JPEG', {'Expires': '0'})}
	print 'Finished read'
	#url = 'http://192.168.0.12:8080/api/images'
	url = 'http://securipi.roscorcoran.com/api/images'
	#payload = {'title': 'tada', 'data': encoded_string}
	#Headers = {'content-type': 'image/JPEG'}
	print 'making request'
	r = requests.post(url, files=files)#, headers=headers)
	print(r.text)
def msg():
	print("Wating for msg")
        msgurl = 'http://securipi.roscorcoran.com/api/control/pi'
	#msgurl = 'http://192.168.0.12:8080/api/control/pi'
	
	try:
		r = requests.get(msgurl, timeout=600)
		if r.text == 'takeapic':
			takeapic()
        	msg()
	except requests.exceptions.Timeout as e:	
		print e
		msg()	
	except requests.exceptions.RequestException as e:    # This is the correct syntax
		print e
		time.sleep(10)
		msg()

try:
	msg()
	#input("Press Enter to continue...")


except KeyboardInterrupt:
    print("KB")  

