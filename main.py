from hx711 import HX711
import logging
import os
import RPi.GPIO as GPIO  # import GPIO
import statistics
import time
import yaml
import argparse

DEFAULT_READOUTS = 5
SCALE_OFFSET = 1
CAL_FACTOR = 1

# SETUP

if not os.path.isfile("configured"):
    print("Your ""configured"" file does not exists. Run system configuration")
    exit()

def load_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main(config):
    # Your main function logic using the config
    print("Configuration:", config)
    # Add your logic here
        
    #Config variables
    VERSION = config["Device"]["Version"]
    DEVICE_ID = config["Device"]["ID"]

    #Pig
    MINIMUM_WEIGHT = config["Pig"]["Min_Weight"]
    LIFT_PIG_FLAG = config["Pig"]["Lift_pig"]
    #Scale
    SCALE_OFFSET = config["Scale"]["Offset"]
    CAL_FACTOR = config["Scale"]["Ratio"]
    SCALE_READOUTS = config["Scale"]["Default_readouts"]

    #Relay
    LOWER_PIN = config["Relay"]["Lift_pin"]
    LIFT_PIN = config["Relay"]["Lower_pin"]

    #Timings
    DELAY_BEFORE_LIFT = config["Timing"]["Before_lift"]
    LIFTING_TIME = config["Timing"]["Lift_time"]
    LOWERING_TIME = config["Timing"]["Lower_time"]
    STATIONARY_PAUSE  = config["Timing"]["Stationary_pause"]

    #Config variables//
    
    #Check to see if the log folder exists and make it if not

    # Specify the folder path
    folder_path = './log'

    #Check if the folder exists
    if not os.path.exists(folder_path):
        # Create the folder if it does not exist
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")

    #Logging stream
    logging.basicConfig(filename = "./log/file_{t}.log".format(t = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())),level=logging.DEBUG, format="%(asctime)s:" + logging.BASIC_FORMAT)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(asctime)s:" + logging.BASIC_FORMAT))
    logging.getLogger().addHandler(console)
    logger = logging.getLogger(__name__)

    timestamp = time.time()
    message_dump = ""

    #Lift Startup log
    output = "Regular Nightly Lift Program"
    log()
    output = "Using hardcoded calibration factor of %i and offset %i" %(CAL_FACTOR, SCALE_OFFSET)
    log()
    output = "The lifting flag is set to %r" %LIFT_PIG_FLAG
    log()

    output = "Piglift startup"
    log()

    #Setup
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
    GPIO.setup(LIFT_PIN, GPIO.OUT)  # Set GPIO pin as output
    GPIO.setup(LOWER_PIN, GPIO.OUT)  # Set GPIO pin as output
    GPIO.output(LOWER_PIN, GPIO.LOW)   # Turn off LED
    GPIO.output(LIFT_PIN, GPIO.LOW)   # Turn off LED


    hx = HX711(pd_sck_pin=19, dout_pin=16)
    hx.power_up()
    output = "Resetting scale..."
    log()
    hx.reset()

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
    GPIO.output(LIFT_PIN, GPIO.HIGH)  # Turn on LED
    time.sleep(LIFTING_TIME)
    GPIO.output(LIFT_PIN, GPIO.LOW)   # Turn off LED

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

    timeout = LOWERING_TIME  # Total timeout in seconds
    interval = 0.1  # Check interval in seconds
    elapsed_time = 0

    GPIO.output(LOWER_PIN, GPIO.HIGH)  # Turn on LED

    num_samples = 3
    while elapsed_time < timeout:
        if get_weight(num_samples) < MINIMUM_WEIGHT:
            break
        elapsed_time += 0.1*num_samples
        time.sleep(interval)
        elapsed_time += interval

    GPIO.output(LOWER_PIN, GPIO.LOW)   # Turn off LED

    output = "The Rig should be on the ground"
    log()

    for _ in range(5): #random number to be updated
        val = get_weight()
        output = f"{val:.3f}"
        log()
        time.sleep(0.05)

    output = "File complete - Exitting"
    log()

    GPIO.cleanup()
    
def log():
    global output, message_dump
    message_dump += f"{output}\n"
    logger.info(output)

def get_weight(readings=DEFAULT_READOUTS):
    """
    Calculates weight by (reading - offset)/calc_factor
    """
    global hx
    raw_read = statistics.mean(hx.get_raw_data(readings))
    weight = round((((raw_read-SCALE_OFFSET)/CAL_FACTOR)**2)**0.5, 3)
    
    return weight
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to run with a specific configuration file.")
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to the configuration file')

    args = parser.parse_args()
    config_file = args.config

    config = load_config(config_file)
    main(config)
