# receiver.py

import os
import sys
import atexit
import signal
import RPi.GPIO as GPIO

# Set up the FIFO
thefifo = 'comms.fifo'
try:
    os.remove(thefifo)
except:
    print("No Fifo present")
os.mkfifo(thefifo)

pin1 = 23
pin2 = 24
low_state = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin1,GPIO.OUT)
GPIO.setup(pin2,GPIO.OUT)
GPIO.output(pin1,low_state)
GPIO.output(pin2,low_state)

led1_state = low_state
led2_state = low_state

# Make sure to clean up after ourselves
#@atexit.register
def cleanup(*args):
    print("Graceful shutdown")
    os.remove(thefifo)
    GPIO.cleanup()

signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

# Go into reading loop
state = 0
while True:
    try:
        with open(thefifo, 'r') as fifo:
            for line in fifo:
                line = line.rstrip().split(" ")
                if(line[0] == "led1"):
                    if(len(line) > 1):
                        state = int(line[1].strip())
                        print("Setting %s state to: %i" % (line[0] , state))
                        if(state>0):
                            led1_state = not low_state
                            GPIO.output(pin1,led1_state)
                        else:
                            led1_state = low_state
                            GPIO.output(pin1,led1_state)
                    else:
                        led1_state = not led1_state
                        GPIO.output(pin1,led1_state)
                        print("Toggle %s" % (line[0]))
                elif(line[0] == "led2"):
                    if(len(line) > 1):
                        state = int(line[1].strip())
                        print("Setting %s state to: %i" % (line[0] , state))
                        if(state>0):
                            led2_state = not low_state
                            GPIO.output(pin2,led2_state)
                        else:
                            led2_state = low_state
                            GPIO.output(pin2,led2_state)
                    else:
                        led2_state = not led2_state
                        GPIO.output(pin2,led2_state)
                        print("Toggle %s" % (line[0]))
                else:
                    print("Command not recognised: %s" % line)
    except(FileNotFoundError):
        break
