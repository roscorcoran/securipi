#!/usr/bin/python
import io
import time
import base64
import picamera
import requests
import json

camera = picamera.PiCamera()

camera.vflip = True
camera.led = True
#camera.start_preview()
camera.capture('image.jpg')
camera.led = False
camera.close()
print 'Closed Cam'

#my_stream = io.BytesIO()
#camera.capture(my_stream, 'jpeg')
#with open('myIm.jpg', 'w+b') as myIm:
#    myIm.write(my_stream.flush())

#camera.hflip = True
#camera.vflip = True
#camera.sharpness = 0
#camera.contrast = 0
#camera.brightness = 50
#camera.saturation = 0
#camera.ISO = 0
#camera.video_stabilization = False
#camera.exposure_compensation = 0
#camera.exposure_mode = 'auto'
#camera.meter_mode = 'average'
#camera.awb_mode = 'auto'
#camera.image_effect = 'none'
#camera.color_effects = None
#camera.rotation = 0
#camera.hflip = False
#camera.vflip = False
#camera.crop = (0.0, 0.0, 1.0, 1.0)

with open('image.jpg', 'r+b') as myIm:
    encoded_string = base64.b64encode(myIm.read())

#with open('b64.txt', 'w') as bim:
#	bim.write(encoded_string)
print 'Finished encode'
url = 'http://192.168.0.12:8080/images'
payload = {'title': 'tada', 'data': encoded_string}
headers = {'content-type': 'application/json'}
print 'making request'

r = requests.post(url, data=json.dumps(payload), headers=headers)
print(r.text)
