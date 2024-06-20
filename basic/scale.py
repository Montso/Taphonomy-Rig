from hx711 import HX711
import RPi.GPIO as GPIO  # import GPIO
import statistics
import time
import argparse

SCALE_OFFSET = 1
CAL_FACTOR = 1

def weigh(offset, factor):
    #Setup
    SCALE_OFFSET = offset
    CAL_FACTOR = factor
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
    hx = HX711(pd_sck_pin=19, dout_pin=16)
    hx.power_up()
    print("Resetting scale...")
    try: 
        hx.reset()
        while True:
            raw_read = statistics.mean(hx.get_raw_data(5))
            weight = round((((raw_read-SCALE_OFFSET)/CAL_FACTOR)**2)**0.5, 3)
            print(weight)
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nApplication Closed by user")


def main():
    parser = argparse.ArgumentParser(description="Printout the values from the Loadcell")
    parser.add_argument('offset', type=float, help='What is the offset of the scale')
    parser.add_argument('cal_factor', type=float, help='The cal_factor for the scale')
    args = parser.parse_args()
    weigh(args.offset,args.cal_factor)

if __name__ == "__main__":
    main()