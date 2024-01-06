import os
# from relay import Relay
from scale import Scale
import statistics
import time


print('==CONFIGURATION==\n')

hx = Scale(dout_pin=14, pd_sck_pin=15)
hx.power_up()
print("")
print("Reset scale")
hx.reset()

print()
input("Press ENTER to begin tare (offset) calculation.")
scale_offset = hx.zero()
scale_offset = int(scale_offset)
print("COMPLETED")
os.system(f"sudo sed -i -E 's/OFFSET:\sfalse/OFFSET: {scale_offset}/' config.yaml")
print("Offset stored in config.yaml\n")

print("Weight calibration.")
input("Hang known mass and press ENTER.")
reading = hx.get_raw_data_mean(10)

print('Mean value from HX711:', reading)
known_weight_grams = input(
    'Write how many grams it was and press ENTER: ')
try:
    value = float(known_weight_grams)
    print(value, 'grams')
except ValueError:
    print('Expected integer or float and I have got:',
            known_weight_grams)

ratio = int(((reading - scale_offset)**2)**0.5 / value)  # calculate the ratio for channel A and gain 128
os.system(f"sudo sed -i -E 's/RATIO:\sfalse/RATIO: {ratio}/' config.yaml")
print("Calibration done.\n")

os.system("touch configured") # add configured flag
print("==CONFIGURATION COMPLETE==")