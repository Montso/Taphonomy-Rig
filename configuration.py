import numpy as np
import os
# from relay import Relay
from scale import Scale
import statistics
import time


print('==Configuration==')

def set_scale_ratio():
    print('Mean value from HX711 subtracted by offset:', reading)
    known_weight_grams = input(
        'Write how many grams it was and press Enter: ')
    try:
        value = float(known_weight_grams)
        print(value, 'grams')
    except ValueError:
        print('Expected integer or float and I have got:',
                known_weight_grams)

    # set scale ratio for particular channel and gain which is
    # used to calculate the conversion to units. Required argument is only
    # scale ratio. Without arguments 'channel' and 'gain_A' it sets
    # the ratio for current channel and gain.
    ratio = reading / value  # calculate the ratio for channel A and gain 128
    os.system(f"sudo sed -i -E 's/RATIO:\sfalse/RATIO: {ratio}/' config.yaml")
    
    print('Ratio is set.')

hx = Scale(dout_pin=14, pd_sck_pin=15)
hx.power_up()
print("reset scale")
hx.reset()

print("tare scale")
hx.zero()
scale_offset = int(hx.offset)
os.system(f"sudo sed -i -E 's/OFFSET:\sfalse/OFFSET: {scale_offset}/' config.yaml")
print("tare stored")


input("Weight calibration in progress. Hang known mass.")
reading = hx.get_raw_data_mean(5)

print('Mean value from HX711:', reading)
known_weight_grams = input(
    'Write how many grams it was and press Enter: ')
try:
    value = float(known_weight_grams)
    print(value, 'grams')
except ValueError:
    print('Expected integer or float and I have got:',
            known_weight_grams)

ratio = ((reading - scale_offset)**2)**0.5 / value  # calculate the ratio for channel A and gain 128
os.system(f"sudo sed -i -E 's/RATIO:\sfalse/RATIO: {ratio}/' config.yaml")
print('Ratio is set.')

os.system("touch configured") # add configured flag
print("configuration complete")