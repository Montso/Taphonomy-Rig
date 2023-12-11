import os
import time

os.system("echo \"led1\" > comms.fifo")
time.sleep(5)
os.system("echo \"led1\" > comms.fifo")
