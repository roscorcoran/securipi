#!/usr/bin/python
import io
import time
import base64
import picamera
#from PIL import Image
import requests
import json
import RPi.GPIO as GPIO ## Import GPIO library
import logging
import logging.handlers
import argparse
import sys
import traceback

# Deafults
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"
LOG_FILENAME = '/var/log/securipi.log'

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="Securipi service")
parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")

# If the log file is specified on the command line then override the default
args = parser.parse_args()
if args.log:
        LOG_FILENAME = args.log

# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
        def __init__(self, logger, level):
                """Needs a logger and a logger level."""
                self.logger = logger
                self.level = level

        def write(self, message):
                # Only log if there is a message (not just a new line)
                if message.rstrip() != "":
                        self.logger.log(self.level, message.rstrip())

# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)

# Loop forever, doing something useful hopefully:

PIR=11


GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
#GPIO.setup(LED, GPIO.OUT, initial=GPIO.HIGH) ## Setup GPIO Pin 7 to OUT
#GPIO.output(LED,True) ## Turn on GPIO pin 7
GPIO.setup(PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Callback
def takeapic(channel):
	#print "Rising edge detected on: " + str(PIR) + "\n"
	
	with picamera.PiCamera() as camera:
		camera.vflip = True
		camera.hflip= True
		camera.led = True
		image_stream = io.BytesIO()
		camera.capture(image_stream, 'jpeg')
		image_stream.seek(0)
        	#image = Image.open(image_stream)
		#camera.capture('image.jpg')
		#Camera.led = False
		camera.close()
		#print 'Closed Cam'
	
	files = {'file': image_stream}
	#files = {'file': ('image', open('image.jpg', 'r+b'), 'image/JPEG', {'Expires': '0'})}
	#print 'Finished read'
	#url = 'http://192.168.0.12:8080/api/images'
	url = 'http://securipi.roscorcoran.com/api/images'
	#payload = {'title': 'tada', 'data': encoded_string}
	#headers = {'content-type': 'image/JPEG'}
	print 'making request'
	r = requests.post(url, files=files)#, headers=headers)
	print(r.text)
	#with open("/tmp/securipi", "w") as f:
        #    f.write("r: "+r+"  "+time.ctime()+"\n")


#GPIO.add_event_detect(PIR, GPIO.RISING, callback=pir_callback, bouncetime=1000)
#GPIO.add_event_detect(PIR, GPIO.RISING, callback=pir_callback, bouncetime=1000)
#try:
#print("Wating for {}".format(PIR))
#GPIO.wait_for_edge(9, GPIO.RISING)
#input("Press Enter to continue...")
#raw_input("press enter to exit ;)")
def msg():
	i=1
        print("Wating for msg")
        msgurl = 'http://securipi.roscorcoran.com/api/control/pi'
        #msgurl = 'http://192.168.0.12:8080/api/control/pi'

        try:
                r = requests.get(msgurl, timeout=6000)
                if r.text == 'takeapic':
                        takeapic(1)
		print r.text
		if r.status_code==200:
			msg()
                        i=1
		else:
                        time.sleep(i*10)
                        i=i+1
			msg()
	except requests.exceptions.HTTPError:
		print "HTTP Error"
                time.sleep(10*i)
                i=i+1
                msg()

	except requests.exceptions.ConnectionError:
                print "Connection Error"
                time.sleep(10*i)
                i=i+1
                msg()
        except requests.exceptions.Timeout as e:
                print e
		print "Message Timeout"
		time.sleep(10*i)
		i=i+1
                msg()
        except requests.exceptions.RequestException as e:    # This is the correct syntax
                print e
                print "Message RequestExc"
		time.sleep(10*i)
		i=i+1
                msg()


def main():
    try:
	GPIO.add_event_detect(PIR, GPIO.RISING, callback=takeapic, bouncetime=1000)
    	msg()
	while True:
                logger.info("sleeping" + time.ctime())
                time.sleep(6000)
                #sys.exit(0)

    except KeyboardInterrupt:
        print "Shutdown requested...exiting"
	GPIO.cleanup()
    except Exception:
        traceback.print_exc(file=sys.stdout)
	GPIO.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    main()
