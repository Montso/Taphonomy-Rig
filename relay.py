import RPi.GPIO as GPIO
from time import sleep

class Relay():

    HIGH = 1
    LOW = 0

    def __init__(self, pin1:int, pin2:int, default_state = LOW):
        """
        Parameters:
        -INx: input pin for relay x 
        -default_state: default relay state
        """
        self.defaul_state = default_state
        self.pin1 = pin1
        self.pin2 = pin2

        # GPIO initilaisation

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin1,GPIO.OUT)
        GPIO.setup(pin2,GPIO.OUT)
        GPIO.output(pin1,default_state)
        GPIO.output(pin2,default_state)

        # initialise relay to NO
        self.led1_state = default_state
        self.led2_state = default_state

    def set_high(self, pin:int):
        match pin:
            case 1:
                GPIO.output(self.pin1,Relay.HIGH)
                self.led1_state = Relay.HIGH
            case 2:
                GPIO.output(self.pin2,Relay.HIGH)
                self.led2_state = Relay.HIGH
        

    def set_low(self, pin):
        match pin:
            case 1:
                GPIO.output(self.pin1,Relay.LOW)
                self.led1_state = Relay.LOW
            case 2:
                GPIO.output(self.pin2,Relay.LOW)
                self.led2_state = Relay.LOW

    def set_state(self, pin, state):
        match state:
            case Relay.HIGH:
                self.set_high(pin)
            case Relay.LOW:
                self.set_low(pin)

    def get_state(self, pin):
        match pin:
            case 1: 
                return self.led1_state
            case 2:
                return self.led2_state
            case _:
                return -1

    def toggle_state(self, pin):
        if pin != 1 or pin != 2:
            print("Pin number should be 1 or 2.")
            quit
        self.set_state(pin, not self.get_state())

class Lift(Relay):
    def __init__(
            self, 
            pin1: int, 
            pin2: int, 
            default_state:[int, bool], 
            lift_pin: int, 
            lower_pin:int):
    
        super().__init__(pin1, pin2, default_state)
        self.lift_pin = lift_pin
        self.lower_pin = lower_pin

    def lift(self, 
             lift_time:int=None, 
             event=None # Using an event flag to stop lifting
             ):

        if not(event == None) and callable(event):
            self.set_high(self.lift_pin)
            while(not event): sleep(10) # slight delay for checking flag 
            self.set_low(self.lift_pin)

        elif not (lift_time == None) and (event == None):
            self.set_high(self.lift_pin)
            sleep(lift_time)
            self.set_low(self.lift_pin)

    def lower(self, 
             lower_time:int=None, 
             event=None # Using an event flag to stop lowering
             ):

        if not(event == None) and callable(event):
            self.set_high(self.lower_pin)
            while(not event): sleep(10) # slight delay for checking flag 
            self.set_low(self.lower_pin)

        elif not (lower_time == None) and (event == None):
            self.set_high(self.lower_pin)
            sleep(lower_time)
            self.set_low(self.lower_pin)

    def hard_stop(self):
        self.set_low(self.lift_pin)
        self.set_low(self.lower_pin)
    