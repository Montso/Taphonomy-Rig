import argparse
import time
import RPi.GPIO as GPIO

# Function to blink the LED
def blink(pin,delay):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    
    try:
        print("Blinking LED, press ctrl+C to stop this program")
        while True:
            print("ON")
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(delay)
            print("OFF")
            GPIO.output(pin, GPIO.LOW)
            time.sleep(delay)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nBlinking stopped by user.")

def main():
    parser = argparse.ArgumentParser(description="Blink an LED with a specified delay.")
    parser.add_argument('pin', type=int, help='Which pin would you like to blink 5 or 22')
    parser.add_argument('delay', type=float, help='Delay time in seconds')
    args = parser.parse_args()
    
    blink(args.pin,args.delay)

if __name__ == "__main__":
    main()
