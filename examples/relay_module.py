import RPi.GPIO as GPIO
import time

class relay_module:

    def __init__(self, pin1, pin2, low_state = True):

        self.low_state = low_state
        self.pin1 = pin1
        self.pin2 = pin2

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin1,GPIO.OUT)
        GPIO.setup(pin2,GPIO.OUT)
        GPIO.output(pin1,low_state)
        GPIO.output(pin2,low_state)

        self.led1_state = low_state
        self.led2_state = low_state

    def set_high(self, which_pin):
        if(which_pin == 1):
            self.led1_state = not self.low_state
            GPIO.output(self.pin1,self.led1_state)
        elif(which_pin == 2):
            self.led2_state = not self.low_state
            GPIO.output(self.pin2,self.led2_state)
        

    def set_low(self, which_pin):
        if(which_pin == 1):
            self.led1_state = self.low_state
            GPIO.output(self.pin1,self.led1_state)
        elif(which_pin == 2):
            self.led2_state = self.low_state
            GPIO.output(self.pin2,self.led2_state)

    def set_state(self, which_pin, which_state):
        if(which_state == 0):
            self.set_low(which_pin)
        elif(which_state == 1):
            self.set_high(which_pin)

    def get_state(self, which_pin):
        if which_pin == 1:
            return self.led1_state
        elif which_pin == 2:
            return self.led2_state
        else:
            return -1

    def toggle_state(self, which_pin):
        self.set_state(which_pin,self.get_state())