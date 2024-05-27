from email.policy import default
from hx711 import HX711
import logging
import numpy as np
import os
from examples.config import LOWER_PIN
from relay import Lift
import RPi.GPIO as GPIO  # import GPIO
from scale import Scale  # import the class HX711
import statistics
import time
import yaml

# SETUP

if not os.path.isfile("configured"):
    print("Your ""configured"" file does not exists. Run system configuration")
    exit()

#Load config data
conf_file = open("default_config.yaml", 'r')
conf = yaml.safe_load(conf_file)
conf_file.close()

#Config variables
VERSION = conf["Device"]["Version"]
DEVICE_ID = conf["Device"]["ID"]

#Pig
AVERAGE_WEIGHT = conf["Pig"]["Avg_Weight"]
LIFT_PIG_FLAG = conf["Pig"]["Lift_pig"]
#Scale
SCALE_OFFSET = conf["Scale"]["OFFSET"]
CAL_FACTOR = conf["Scale"]["RATIO"]
SCALE_READOUTS = conf["Scale"]["Default_readouts"]

#Relay
LOWER_PIN = conf["Relay"]["LOWER_PIN"]
LIFT_PIN = conf["Relay"]["LIFT_PIN"]
LIFT_DELAY = conf["Relay"]["DELAY"]

#Timings
DELAY_BEFORE_LIFT = conf["Timing"]["Before_lift"]
LIFTING_TIME = conf["Timing"]["Lift_time"]
LOWERING_TIME = conf["Timing"]["Lowering_time"]
STATIONARY_PAUSE  = conf["Timing"]["Stationary_pause"]

#Config variables//


#Logging stream
logging.basicConfig(filename = "./log/file_{t}.log".format(t = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())),level=logging.DEBUG, format="%(asctime)s:" + logging.BASIC_FORMAT)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter("%(asctime)s:" + logging.BASIC_FORMAT))
logging.getLogger().addHandler(console)
logger = logging.getLogger(__name__)

timestamp = time.time()
message_dump = ""

def log():
    global output, message_dump
    message_dump += f"{output}\n"
    logger.info(output)

#Lift Startup log
output = "Regular Nightly Lift Program"
log()
output = "Using hardcoded calibration factor of %i and offset %i" %(CAL_FACTOR, SCALE_OFFSET)
log()
output = "The lifting flag is set to %r" %LIFT_PIG_FLAG
log()
time.sleep(2)

output = "Piglift startup"
log()

#Setup
GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering

platform = Lift(
    pin1=22,
    pin2=5,
    default_state=False,
    lift_pin=LIFT_PIN,
    lower_pin=LOWER_PIN) # Handles the wrench lifting/lowering

hx = HX711(pd_sck_pin=19, dout_pin=16)
hx.power_up()
output = "Resetting scale..."
log()
hx.reset()

def get_weight(readings=SCALE_READOUTS):
    """
    Calculates weight by (reading - offset)/calc_factor
    """
    global hx
    raw_read = hx.get_raw_data_mean(SCALE_READOUTS)
    weight = round((((raw_read-SCALE_OFFSET)/CAL_FACTOR)**2)**0.5, 3)
    
    return weight

#SETUP//

output = "Printing %i test readings"%SCALE_READOUTS
log()

for _ in range(5): #random number to be updated
    val = get_weight()
    output = str(val)
    log()
    time.sleep(0.05)

#Lift the rig
#LIFT Procedure
output = "performing a lift in %i seconds" % DELAY_BEFORE_LIFT
log()
time.sleep(DELAY_BEFORE_LIFT)
platform.lift(LIFTING_TIME)

#Halt at top
output = "Halting at the top for %i seconds" % STATIONARY_PAUSE
log()
time.sleep(STATIONARY_PAUSE)

for _ in range(5): #random number to be updated
    val = get_weight()
    output = f"{val:.3f}"
    log()
    time.sleep(0.05)


#Lower the rig
platform.lower(LOWERING_TIME)

output = "The Rig should be on the ground"
log()

for _ in range(5): #random number to be updated
    val = get_weight()
    output = f"{val:.3f}"
    log()
    time.sleep(0.05)

output = "File complete"
log()

GPIO.cleanup()