from collections import namedtuple
from enum import IntEnum
import spidev
import sys
from time import sleep
import yaml

# with open('./config.yaml', 'r') as file:
#     CONFIGS = yaml.safe_load(file)
# FLOAT_DP = CONFIGS["float_precision"]
FLOAT_DP = 3

class Power():
    class ADC_PIN(IntEnum):
        ADC0, ADC1, ADC2, ADC3, ADC4, ADC5, ADC6, ADC7 = list(range(8))
        def __int__(self):
            self.value
    
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
        self.spi.xfer2([0])

    def read_adc(self, channel) -> int:
        channel = channel
        msg = [channel<<3, 0x00] 
        returnchars = self.spi.xfer2(msg)

        returnchars = self.spi.xfer2(msg)
        value = returnchars[0]*64 + returnchars[1]/4
        return value
    
    def read_analog_value(self, channel) -> float:
        adc_val = self.read_adc(channel)
        analog_val = Power.ANALOG_REF*adc_val/(1024 -1)

        return analog_val        

    def read_temp(self) -> float:
        Voffs = 500e-3
        Tc = 10e-3
        Tinfl = 0
        get_temp = lambda Vout: ((Vout - Voffs)/Tc) + Tinfl

        temp_vout = self.read_analog_value(Power.SENSE_TEMP)
        temp = get_temp(temp_vout)

        return temp

    def read_vin(self) -> float:
        sense = self.read_analog_value(Power.VIN)
        return round(sense, FLOAT_DP)

    def read_sense_batt(self) -> float:
        sense = self.read_analog_value(Power.SENSE_BATT)
        return round(sense, FLOAT_DP)
    
    def read_sense_3v3(self) -> float:
        sense = self.read_analog_value(Power.SENSE_3V3)*2
        return round(sense, FLOAT_DP)

    def read_ref_2v5(self) -> float:
        sense = self.read_analog_value(Power.REF_2V5)
        return round(sense, FLOAT_DP)


if __name__ == "__main__":
    power = Power()
    print(power.read_ref_2v5())
    sys.exit()
