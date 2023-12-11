from relay_module import relay_module
import time

relay = relay_module(23,24) #Pins for the relay module
relay.set_high(2)
time.sleep(1)
relay.set_low(2)