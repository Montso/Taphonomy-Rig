from hx711 import HX711
import time
import statistics
import numpy as np
import os
from relay_module import relay_module

#HARDWARE DEFINES
LIFT_PIN = 1
LOWER_PIN = 2


scale_offset = -94186                                                               #default starting value
cal_factor = -13966                                                                 # conversion to kg

#TIMING
lifting_time = 2
peaceful_pause = 5
sway_preventing_delay = 10

#READOUTS
reading_prints = 10

print("Regular Nightly Lift Program")
print("Using hardcoded calibration factor of %i and offset %i" %(cal_factor, scale_offset))


def remove_outliers(input_data):
    elements = np.array(input_data)
    mean = np.mean(elements)
    sd = np.std(elements)
    length = []
    index_max_matrix = []
    if(sd>40000): #was abs(mean)#this should be some hardcoded value, rather than the mean, but because I dont know parameters of the scales Im working with, I thought this was alright
        for x in input_data:
            row = []
            for y in input_data:
                row.append((x-y)**2)
            index_max = max(range(len(row)), key=row.__getitem__)
            index_max_matrix.append(index_max)
            length.append(row)
        #print(length)
        print("Erased a value" , index_max_matrix)
        try:
            input_data.remove(input_data[statistics.mode(index_max_matrix)])
        except:
            print("Had an error in the mode")
    return input_data

print("Piglift startup")

relay = relay_module(23,24) #Pins for the relay module

hx = HX711(5,6)
hx.power_up()
print("reset scale")
hx.reset()

print("Printing %i readings:" % reading_prints)
#time.sleep(peaceful_pause)
for i in range(0,20):
    raw_read = hx.get_raw_data(5)
    processed_read = remove_outliers(raw_read)
    #processed_read = raw_read
    val = round(((statistics.mean(processed_read)-scale_offset)/cal_factor),3)
    print(processed_read, val)
    time.sleep(0.05)

print("performing a lift in %i seconds" % peaceful_pause)
time.sleep(peaceful_pause)
relay.set_high(LIFT_PIN)
time.sleep(lifting_time)
relay.set_low(LIFT_PIN)

print("waiting for %i seconds to stop sway" % sway_preventing_delay)
time.sleep(sway_preventing_delay)

for i in range(0,20):
    raw_read = hx.get_raw_data(5)
    processed_read = remove_outliers(raw_read)
    #processed_read = raw_read
    val = round(((statistics.mean(processed_read)-scale_offset)/cal_factor),3)
    print(processed_read, val)
    time.sleep(0.05)

current_weight = 100
current_time = time.process_time()
print(current_time)
relay.set_high(LOWER_PIN)
while((current_weight > 8) and (time.process_time() - current_time < lifting_time)):
    raw_read = hx.get_raw_data(3)
    processed_read = remove_outliers(raw_read)
    current_weight = round(((statistics.mean(processed_read)-scale_offset)/cal_factor),3)
final_time = time.process_time()
print(final_time)
print("Lowering time of %d" % (final_time-current_time))
relay.set_low(LOWER_PIN)

time.sleep(peaceful_pause)
for i in range(0,3):
    raw_read = hx.get_raw_data(5)
    processed_read = remove_outliers(raw_read)
    #processed_read = raw_read
    val = round(((statistics.mean(processed_read)-scale_offset)/cal_factor),3)
    print(processed_read, val)
    time.sleep(0.05)
