#Pi HAT project#

This code is to run on the Taphonomy rig. It includes code for the [Pi HAT project.](https://github.com/montso/Pi-HAT)

##First time setup on the Pi is:##

`sudo apt-get update`
`sudo apt-get install -y python3-pip`
`sudo apt-get install -y git`

`git clone https://github.com/Montso/Taphonomy-Rig.git`

`sudo python3 -m pip install -r requirements.txt --break-system-packages`

Then in Taphonomy-Rig/ you have 2 options:
Testing or perform a lift:

###Lifting:###

`python3 main.py`

This should fail initially as it informs you that a configuration hasnt been performed.

To do that you type:

`python3 configuration.py`

It should go through the instructions for you.

After that it creates an empty file called "configured" that is how main.py knows whether its been run or not. Deleting this file will require configuration to be run again.

Changing the values in config.yaml will change the operations of the device on each main.py operation.

The files will be saved in Taphonomy-Rig/log/

###Testing:###
If you want to test, there is a folder Taphonomy-Rig/basic/ which has blink scripts for the pins required for lifting and lowering.
And some code to test the scale - to come.