from hx711 import HX711
import time
import statistics
import numpy as np
import os
from relay_module import relay_module

err = 50

def remove_outliers(input_data):
    elements = np.array(input_data)
    mean = np.mean(elements)
    sd = np.std(elements)
    length = []
    index_max_matrix = []
    if(sd>abs(mean)):
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

LIFT_PIN = 1
LOWER_PIN = 2

hx = HX711(5,6)
hx.power_up()
print("reset scale")
hx.reset()
print("tare scale")
scale_offset = 10                                                                   #default starting value
cal_factor = 13966                                                                  # conversion to kg
prev_reading = statistics.mean(remove_outliers(hx.get_raw_data(10)))
#prev_reading = statistics.mean(hx.get_raw_data(10))
cnt = 0
convergence_rate = 0.8
while (pow(pow((scale_offset - prev_reading),2),0.5)>err):
    prev_prev = prev_reading
    prev_reading = statistics.mean(remove_outliers(hx.get_raw_data(10)))
    #prev_reading = statistics.mean(hx.get_raw_data(10))
    if(pow(pow(prev_prev-prev_reading,2),0.5)<0.1*cal_factor): #IF the difference MSE between the 2 prev < appox 100g
        scale_offset = scale_offset*convergence_rate + (1-convergence_rate)*prev_reading
        cnt = cnt + 1
        print("%i: %d" % (cnt,scale_offset))
print("Scale calibrated")
time.sleep(3)
print("Printing 20 readings:")
time.sleep(2)
for i in range(0,20):
    raw_read = hx.get_raw_data(5)
    processed_read = remove_outliers(raw_read)
    #processed_read = raw_read
    val = round(((statistics.mean(processed_read)-scale_offset)/cal_factor),3)
    print(processed_read, val)
    time.sleep(0.05)

print("performing a lift in 5 seconds")
time.sleep(5)
relay.set_high(LIFT_PIN)
time.sleep(2)
relay.set_low(LIFT_PIN)

print("waiting for 10 seconds to stop sway")
time.sleep(10)

for i in range(0,20):
    raw_read = hx.get_raw_data(5)
    processed_read = remove_outliers(raw_read)
    #processed_read = raw_read
    val = round(((statistics.mean(processed_read)-scale_offset)/cal_factor),3)
    print(processed_read, val)
    time.sleep(0.05)

relay.set_high(LOWER_PIN)
time.sleep(2)
relay.set_low(LOWER_PIN)

for i in range(0,3):
    raw_read = hx.get_raw_data(5)
    processed_read = remove_outliers(raw_read)
    #processed_read = raw_read
    val = round(((statistics.mean(processed_read)-scale_offset)/cal_factor),3)
    print(processed_read, val)
    time.sleep(0.05)
