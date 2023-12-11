#Global flags
send_emails = True
lift_pig = True

#Email Parameters
email_address = 'piglift.uct@gmail.com'
password = 'VickyDevinMaxKara'
#Plain text which is a BIG no no, but time constraints
receiver_list = {"justin.pead@uct.ac.za", "karasadams3@gmail.com","d.finaughty@kent.ac.uk"}
port = 587 # for starttls
smtp_server = "smtp.gmail.com"

#HARDWARE DEFINES
LIFT_PIN = 1
LOWER_PIN = 2

scale_offset = 24400                                                               #default starting value
cal_factor = 22775                                                                 # conversion to kg
#TIMING
lifting_time = 2
peaceful_pause = 5
sway_preventing_delay = 10
reading_count = 20
rig_on_ground_threshold = 15

#READOUTS
reading_prints = 10
