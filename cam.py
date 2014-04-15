#!/usr/bin/python
import picamera

camera = picamera.PiCamera()

camera.vflip = True

camera.capture('image.jpg')

#camera.hflip = True
#camera.vflip = True
