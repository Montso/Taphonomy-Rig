from hx711 import HX711
import numpy as np
import statistics

class Scale(HX711):

    def __init__(self,    
            dout_pin=21, pd_sck_pin=20, gain=128, channel='A'):
        super().__init__(dout_pin=dout_pin, pd_sck_pin=pd_sck_pin, gain=gain, channel=channel)

        self.offset = 2500
        #tare calibration variables
        self.err = 50

    def get_raw_data(self, readings):
        raw_data = super().get_raw_data(readings)
        data = self.remove_outliers(raw_data)

        return data
    
    def get_raw_data_mean(self, readings):
        raw_data = self.get_raw_data(readings)
        return statistics.mean(raw_data)

    def remove_outliers(self, input_data):
        elements = np.array(input_data)
        mean = np.mean(elements)
        sd = np.std(elements)
        length = []
        index_max_matrix = []
        if(sd>0.5*mean):
            for x in input_data:
                row = []
                for y in input_data:
                    row.append((x-y)**2)
                index_max = max(range(len(row)
                ), key=row.__getitem__)
                index_max_matrix.append(index_max)
                length.append(row)
            print(length)
            # print("Erased a value" , index_max_matrix) 
            #will keep for logs
            input_data.remove(input_data[statistics.mode(index_max_matrix)])
        return input_data
            
    def zero(self, readings=30):
        scale_offset = self.offset                                                                   #default starting value
        ratio = 32000                                                                  # conversion to kg
        prev_reading = self.get_raw_data_mean(10)
        cnt = 0
        convergence_rate = 0.8
        mse = lambda x, y:statistics.sqrt((x - y)**2)
        while (mse(scale_offset, prev_reading)>self.err):
            prev_prev = prev_reading
            prev_reading = self.get_raw_data_mean(10)
            if(mse(prev_prev, prev_reading)<0.1*ratio): #IF the difference MSE between the 2 prev < appox 100g
                scale_offset = scale_offset*convergence_rate + (1-convergence_rate)*prev_reading
                cnt = cnt + 1
                print("%i: %d" % (cnt,scale_offset))
        
        result = self.get_raw_data(readings)
        self.offset = scale_offset
