import RPi.GPIO as GPIO

class relay_module():

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
                GPIO.output(self.pin1,relay_module.HIGH)
                self.led1_state = relay_module.HIGH
            case 2:
                GPIO.output(self.pin2,relay_module.HIGH)
                self.led2_state = relay_module.HIGH
        

    def set_low(self, pin):
        match pin:
            case 1:
                GPIO.output(self.pin1,relay_module.LOW)
                self.led1_state = relay_module.LOW
            case 2:
                GPIO.output(self.pin2,relay_module.LOW)
                self.led2_state = relay_module.LOW

    def set_state(self, pin, state):
        match state:
            case relay_module.HIGH:
                self.set_high(pin)
            case relay_module.LOW:
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