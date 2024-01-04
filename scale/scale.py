from hx711 import HX711
import numpy as np
import statistics

class Scale(HX711):

    def __init__(self,    
            dout_pin=21, pd_sck_pin=20, gain_channel_A=128, select_channel='A'):
        super().__init(dout_pin=dout_pin, pd_sck_pin=pd_sck_pin, gain_channel_A=gain_channel_A, select_channel=select_channel)

        self.set_data_filter(Scale.remove_outliers)

        #tare calibra
    

    def remove_outliers(cls, input_data):
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
            
    def tare_calibration(self):
        err=50
        scale_offset = 10                                                                   #default starting value
        ratio = 32000                                                                  # conversion to kg
        prev_reading = self.get_raw_data_mean(10)
        cnt = 0
        convergence_rate = 0.8
        while (abs(scale_offset - prev_reading))>err:
            prev_prev = prev_reading
            prev_reading = self.get_raw_data_mean(10)
            if((abs(prev_prev-prev_reading))<0.1*ratio): #IF the difference MSE between the 2 prev < appox 100g
                scale_offset = scale_offset*convergence_rate + (1-convergence_rate)*prev_reading
                cnt = cnt + 1
                print("%i: %d" % (cnt,scale_offset))

        self.set_scale_ratio(ratio)
