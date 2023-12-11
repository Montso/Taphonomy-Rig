from hx711 import HX711
import time
import statistics
import smtplib, ssl
import numpy as np
import os
import config as conf
import logging
from relay_module import relay_module

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

logging.basicConfig(filename = "./log/file_{t}.log".format(t = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())),level=logging.DEBUG, format="%(asctime)s:" + logging.BASIC_FORMAT)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter("%(asctime)s:" + logging.BASIC_FORMAT))
logging.getLogger().addHandler(console)
logger = logging.getLogger(__name__)

version = "1.0"
device_id = "1"

timestamp = time.time()
average_weight = 42
message_dump = ""

output = "Regular Nightly Lift Program"
message_dump += output+"\n"
logger.info(output)
output = "Using hardcoded calibration factor of %i and offset %i" %(conf.cal_factor, conf.scale_offset)
message_dump += output+"\n"
logger.info(output)
output = "The lifting flag is set to %r" %conf.lift_pig
message_dump += output+"\n"
logger.info(output)
output = "The email flag is set to %r\n"%conf.send_emails
message_dump += output+"\n"
logger.info(output)
time.sleep(2)

output = "Piglift startup"
message_dump += output+"\n"
logger.info(output)

relay = relay_module(23,24) #Pins for the relay module

hx = HX711(5,6)
hx.power_up()
output = "reset scale"
message_dump += output+"\n"
logger.info(output)

hx.reset()

output = "Printing %i readings:" % conf.reading_prints
message_dump += output + "\n"
logger.info(output)

#time.sleep(peaceful_pause)
for i in range(0,conf.reading_count):
    raw_read = hx.get_raw_data(5)
    processed_read = remove_outliers(raw_read)
    #processed_read = raw_read
    val = round(((statistics.mean(processed_read)-conf.scale_offset)/conf.cal_factor),3)
    output = str(val)
    message_dump += output + "\n"
    logger.info(output)
    time.sleep(0.05)

output = "performing a lift in %i seconds" % conf.peaceful_pause
message_dump += output+"\n"
logger.info(output)
time.sleep(conf.peaceful_pause)
if(conf.lift_pig):
    relay.set_high(conf.LIFT_PIN)
    time.sleep(conf.lifting_time)
    relay.set_low(conf.LIFT_PIN)


output = "waiting for %i seconds to stop sway" % conf.sway_preventing_delay
message_dump += output+"\n"
logger.info(output)
time.sleep(conf.sway_preventing_delay)
average = 0
for i in range(0,conf.reading_count):
    raw_read = hx.get_raw_data(5)
    processed_read = remove_outliers(raw_read)
    #processed_read = raw_read
    val = round(((statistics.mean(processed_read)-conf.scale_offset)/conf.cal_factor),3)	
    average+=val
    output = str(val)
    message_dump += output+"\n"
    logger.info(output)
    time.sleep(0.05)
average_weight = average/conf.reading_count
current_weight = average_weight
current_time = time.process_time()
logger.info(current_time)
if(conf.lift_pig):
    relay.set_high(conf.LOWER_PIN)

while((current_weight > conf.rig_on_ground_threshold) and (time.process_time() - current_time < conf.lifting_time)):
    raw_read = hx.get_raw_data(3)
    processed_read = remove_outliers(raw_read)
    current_weight = round(((statistics.mean(processed_read)-conf.scale_offset)/conf.cal_factor),3)
final_time = time.process_time()
logger.info(final_time)
print("Lowering time of %d" % (final_time-current_time))
if(conf.lift_pig):
    relay.set_low(conf.LOWER_PIN)

time.sleep(conf.peaceful_pause)
for i in range(0,3):
    raw_read = hx.get_raw_data(5)
    processed_read = remove_outliers(raw_read)
    #processed_read = raw_read
    val = round(((statistics.mean(processed_read)-conf.scale_offset)/conf.cal_factor),3)
    output = str(val)
    message_dump += output+"\n"
    logger.info(output)
    time.sleep(0.05)

message = """\
Subject: Pig Lift Auto Generated Email

Hello Pig Team, this is device %s operating on version %s\n\nReading taken at time %i\n

The weight for the lift was: %f\n
%s

This message is sent from Python.""" % (device_id, version, timestamp, average_weight, message_dump)

logger.info(message)

context = ssl.create_default_context()
with smtplib.SMTP(conf.smtp_server, conf.port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(conf.email_address, conf.password)
    if(conf.send_emails):
        for receiver_address in conf.receiver_list:
            server.sendmail(conf.email_address, receiver_address, message)
            print("Sent email to %s"%receiver_address)
    else:
        print("No emails sent")
