#!/usr/bin/python
import RPi.GPIO as GPIO ## Import GPIO library
import time
PIR=11
#LED=4

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
#GPIO.setup(LED, GPIO.OUT, initial=GPIO.HIGH) ## Setup GPIO Pin 7 to OUT
#GPIO.output(LED,True) ## Turn on GPIO pin 7
GPIO.setup(PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Callback
def pir_callback(channel):  
    print "Rising edge detected on: " + str(PIR) + "\n"
    Blink(20,0.1) 

GPIO.add_event_detect(PIR, GPIO.RISING, callback=pir_callback, bouncetime=300) 
##Define a function named Blink()
def Blink(numTimes,speed):
	print "Called"
	for i in range(0,numTimes):## Run loop numTimes
		#print "Iteration " + str(i+1)## Print current loop
		#GPIO.output(LED,True)## Switch on pin 7
		time.sleep(speed)## Wait
		#GPIO.output(LED,False)## Switch off pin 7
		#time.sleep(speed)## Wait
	#print "Done" ## When loop is complete, print "Done"
	#GPIO.cleanup()

## Ask user for total number of blinks and length of each blink
#iterations = raw_input("Enter total number of times to blink: ")
#speed = raw_input("Enter length of each blink(seconds): ")

## Start Blink() function. Convert user input from strings to numeric data types and pass to Blink() as parameters
#Blink(int(iterations),float(speed))


try:
    print("Wating for {}".format(PIR)) 
    #GPIO.wait_for_edge(17, GPIO.RISING)
    input("Press Enter to continue...")  
    
  
except KeyboardInterrupt:  
    print("KB")
    #GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  
