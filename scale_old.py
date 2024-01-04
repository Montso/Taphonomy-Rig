from scale import Scale
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

hx = Scale(dout_pin=14, pd_sck_pin=15)
hx.power_up()
print("reset scale")
hx.reset()
print("tare scale")
hx.zero()
while(True):
    processed_read = hx.get_raw_data(10)
    val = round(((statistics.mean(processed_read)-hx.offset)/cal_factor),3)
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
            # os.system("echo \"led1\" >> comms.fifo")
            pass
    time.sleep(0.05)
