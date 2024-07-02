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
hx = HX711(pd_sck_pin=19, dout_pin=16)

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

    #Lift Startup log
    output = "Regular Nightly Lift Program\n"
    logger.info(output)
    output = "Using hardcoded calibration factor of %i and offset %i\n" %(CAL_FACTOR, SCALE_OFFSET)
    logger.info(output)
    output = "The lifting flag is set to %r\n" %LIFT_PIG_FLAG
    logger.info(output)

    output = "Piglift startup\n"
    logger.info(output)

    #Setup
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
    GPIO.setup(LIFT_PIN, GPIO.OUT)  # Set GPIO pin as output
    GPIO.setup(LOWER_PIN, GPIO.OUT)  # Set GPIO pin as output
    GPIO.output(LOWER_PIN, GPIO.LOW)   # Turn off LED
    GPIO.output(LIFT_PIN, GPIO.LOW)   # Turn off LED


    hx = HX711(pd_sck_pin=19, dout_pin=16)
    hx.power_up()
    output = "Resetting scale...\n"
    logger.info(output)
    hx.reset()

    #SETUP//

    output = "Printing %i test readings\n"%SCALE_READOUTS
    logger.info(output)

    for _ in range(5): #random number to be updated
        val = get_weight()
        output = "%s\n"%str(val)
        logger.info(output)
        time.sleep(0.05)

    #Lift the rig
    #LIFT Procedure
    output = "performing a lift in %i seconds\n" % DELAY_BEFORE_LIFT
    logger.info(output)
    time.sleep(DELAY_BEFORE_LIFT)
    GPIO.output(LIFT_PIN, GPIO.HIGH)  # Turn on LED
    time.sleep(LIFTING_TIME)
    GPIO.output(LIFT_PIN, GPIO.LOW)   # Turn off LED

    #Halt at top
    output = "Halting at the top for %i seconds\n" % STATIONARY_PAUSE
    logger.info(output)
    time.sleep(STATIONARY_PAUSE)

    for _ in range(5): #random number to be updated
        val = get_weight()
        output = f"{val:.3f}\n"
        logger.info(output)
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

    output = "The Rig should be on the ground\n"
    logger.info(output)

    for _ in range(5): #random number to be updated
        val = get_weight()
        output = f"{val:.3f}\n"
        logger.info(output)
        time.sleep(0.05)

    output = "File complete - Exitting\n"
    logger.info(output)

    GPIO.cleanup()

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
