from hx711 import HX711
import time
import statistics
import numpy as np
import os

err = 50

light_state = False
on_scale = False
on_scale_confidence = 0
on_scale_confidence_compare = 3
prev_on_scale = False

def remove_outliers(input_data):
    elements = np.array(input_data)
    mean = np.mean(elements)
    sd = np.std(elements)
    length = []
    index_max_matrix = []
    if(sd>mean):
        for x in input_data:
            row = []
            for y in input_data:
                row.append((x-y)**2)
            index_max = max(range(len(row)), key=row.__getitem__)
            index_max_matrix.append(index_max)
            length.append(row)
        print(length)
        print("Erased a value" , index_max_matrix)
        input_data.remove(input_data[statistics.mode(index_max_matrix)])
    return input_data

hx = HX711(5,6)
hx.power_up()
print("reset scale")
hx.reset()
print("tare scale")
scale_offset = 10                                                                   #default starting value
cal_factor = 32000                                                                  # conversion to kg
prev_reading = statistics.mean(remove_outliers(hx.get_raw_data(10)))
cnt = 0
convergence_rate = 0.8
while (pow(pow((scale_offset - prev_reading),2),0.5)>err):
    prev_prev = prev_reading
    prev_reading = statistics.mean(remove_outliers(hx.get_raw_data(10)))
    if(pow(pow(prev_prev-prev_reading,2),0.5)<0.1*cal_factor): #IF the difference MSE between the 2 prev < appox 100g
        scale_offset = scale_offset*convergence_rate + (1-convergence_rate)*prev_reading
        cnt = cnt + 1
        print("%i: %d" % (cnt,scale_offset))
while(True):
    raw_read = hx.get_raw_data(3)
    processed_read = remove_outliers(raw_read)
    val = round(((statistics.mean(processed_read)-scale_offset)/cal_factor),3)
    print(processed_read, val)
    if(val>1):
        on_scale = True
    else:
        on_scale = False
    if(prev_on_scale != on_scale):
        on_scale_confidence = on_scale_confidence+1
    else:
        if(on_scale_confidence>=1):
            on_scale_confidence = on_scale_confidence-1
    state_change = 0
    if(on_scale_confidence >= on_scale_confidence_compare):
        on_scale_confidence=0
        state_change = 1
        prev_on_scale = on_scale
    if(state_change):
        state_change=0
        if(on_scale):
            os.system("echo \"led1\" >> comms.fifo")
    time.sleep(0.05)
