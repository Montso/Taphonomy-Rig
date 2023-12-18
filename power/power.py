from collections import namedtuple
from enum import Enum
import spidev
import sys
import time


class Power():
    class ADC_PIN(Enum):
        ADC0, ADC1, ADC2, ADC3, ADC4, ADC5, ADC6, ADC7 = range(0, 8)
    
    VIN = ADC_PIN.ADC0
    IN0 = ADC_PIN.ADC2 #General purpose pin for future use
    REF_2V5 = ADC_PIN.ADC4
    SENSE_3V3 = ADC_PIN.ADC5
    SENSE_BATT = ADC_PIN.ADC6
    SENSE_TEMP = ADC_PIN.ADC7

    ANALOG_REF = 5.0

    def __init__(self, bus=0, device=0, max_speed_hz=1000000) -> None:
        self.bus = bus
        self.device = device
        self.max_speed_hz = max_speed_hz

        #Initiate spi interface
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = self.max_speed_hz

        self.clear_buffer()


    def clear_buffer(self) -> None:
        self.spi.xfer2(0)

    def read_adc(self, channel = 0) -> int:
        msg = [channel<<3, 0x00] 
        returnchars = spi.xfer2(msg)

        returnchars = spi.xfer2(msg)
        value = returnchars[0]*64 + returnchars[1]/4
        return value
    
    def read_analog_value(self, channel=0) -> float:
        adc_val = self.read_adc(channel)
        analog_val = Power.ANALOG_REF/adc_val/(1024 -1)

        return analog_val        

if __name__ == "__main__":
    # read_adc()
    pass