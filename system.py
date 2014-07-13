#!/usr/bin/python
import io
import time
import base64
import picamera
import requests
import json
import RPi.GPIO as GPIO ## Import GPIO library
PIR=11


GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
#GPIO.setup(LED, GPIO.OUT, initial=GPIO.HIGH) ## Setup GPIO Pin 7 to OUT
#GPIO.output(LED,True) ## Turn on GPIO pin 7
GPIO.setup(PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Callback
def pir_callback(channel):
	print "Rising edge detected on: " + str(PIR) + "\n"
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

GPIO.add_event_detect(PIR, GPIO.RISING, callback=pir_callback, bouncetime=1000)

try:
    print("Wating for {}".format(PIR))
    #GPIO.wait_for_edge(9, GPIO.RISING)
    #input("Press Enter to continue...")
    raw_input("press enter to exit ;)")


except KeyboardInterrupt:
    print("KB")
    #GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  

