import RPi.GPIO as GPIO
import time

# Set up the GPIO pin
LED_PIN = 22  # GPIO pin 22
BLINK_DELAY = 1  # 1 second delay

def setup():
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
    GPIO.setup(LED_PIN, GPIO.OUT)  # Set GPIO pin as output

def blink():
    try:
        while True:
            GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on LED
            time.sleep(BLINK_DELAY)
            GPIO.output(LED_PIN, GPIO.LOW)   # Turn off LED
            time.sleep(BLINK_DELAY)
    except KeyboardInterrupt:
        pass  # Allow clean exit on Ctrl+C

def cleanup():
    GPIO.cleanup()  # Reset GPIO settings

if __name__ == '__main__':
    setup()
    blink()
    cleanup()