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
	
	with open('image.jpg', 'r+b') as myIm:
		encoded_string = base64.b64encode(myIm.read())

	print 'Finished encode'
	url = 'http://securipi.roscorcoran.com/api/images'
	payload = {'title': 'tada', 'data': encoded_string}
	headers = {'content-type': 'application/json'}
	print 'making request'
	
	r = requests.post(url, data=json.dumps(payload), headers=headers)
	print(r.text)

GPIO.add_event_detect(PIR, GPIO.RISING, callback=pir_callback, bouncetime=300)

try:
    print("Wating for {}".format(PIR))
    #GPIO.wait_for_edge(9, GPIO.RISING)
    #input("Press Enter to continue...")
    raw_input("press enter to exit ;)")


except KeyboardInterrupt:
    print("KB")
    #GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  

