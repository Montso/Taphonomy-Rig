
from hx711 import HX711
import numpy as np
import statistics

class Scale(HX711):

    def __init__(self,    
            dout_pin=21, pd_sck_pin=20, gain=128, channel='A'):
        super().__init__(dout_pin=dout_pin, pd_sck_pin=pd_sck_pin, gain=gain, channel=channel)

        #tare configs
        self.offset = 2500 #random initial value
        self.err = 50 #convergence error for tare calc
        self.convergence_rate = 0.8 #convergence rate for tare calculation
        self.ratio = 32000 #hardcoded ratio for sanity check

    def get_raw_data(self, readings=5):
        """
        Overriding hx711 get_raw_data to apply data filtering
        Returns: list of readings, default 5 readings
        """
        raw_data = super().get_raw_data(readings)
        data = self.remove_outliers(raw_data)

        return data
    
    def get_raw_data_mean(self, readings):
        """
        Return a mean of the load cell raw data
        """
        raw_data = self.get_raw_data(readings)
        return statistics.mean(raw_data)

    def remove_outliers(self, input_data):
        """
        Outlier detection using modal index of number with biggest square difference 
        """
        elements = np.array(input_data)
        mean = np.mean(elements)
        sd = np.std(elements)
        col = []
        index_max_matrix = []
        if(sd>0.5*mean):
            for x in input_data:
                row = []
                for y in input_data:
                    row.append((x-y)**2) #get per element square difference 
                index_max = max(range(len(row)
                ), key=row.__getitem__)
                index_max_matrix.append(index_max)
                col.append(row)
    
            input_data.remove(input_data[statistics.mode(index_max_matrix)]) #remove each outlier
            print("Erased a value" , set(index_max_matrix))
        return input_data
            
    def zero(self):
        """

        """
        scale_offset = self.offset                                                               # conversion to kg
        prev_reading = self.get_raw_data_mean(10)
        cnt = 0
        mse = lambda x, y:statistics.sqrt((x - y)**2)
        while (mse(scale_offset, prev_reading)>self.err):
            prev_prev = prev_reading
            prev_reading = self.get_raw_data_mean(10)
            if(mse(prev_prev, prev_reading)<0.1*self.ratio): #If the difference MSE between the 2 prev < appox 100g
                scale_offset = scale_offset*self.convergence_rate + (1-self.convergence_rate)*prev_reading
                cnt = cnt + 1
                print("%i: %d" % (cnt,scale_offset))
    
        self.offset = scale_offset
        return scale_offset
