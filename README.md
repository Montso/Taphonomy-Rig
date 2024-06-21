# Pi HAT project

This code is to run on the Taphonomy rig. It includes code for the [Pi HAT project.](https://github.com/montso/Pi-HAT)

## First time setup on the Pi is:

`sudo apt-get update`

`sudo apt-get install -y python3-pip git`

`sudo timedatectl set-timezone Africa/Johannesburg`

`git clone https://github.com/Montso/Taphonomy-Rig.git`

`cd Taphonomy-Rig/`

## Then in Taphonomy-Rig/ folder

You just need to install the initial packages. That can be done with the following line.

`sudo python3 -m pip install -r requirements.txt --break-system-packages`

Now its ready for operation

you have 2 options; Testing or Lifting:

### Lifting:

`python3 main.py`

This should fail initially as it informs you that a configuration hasnt been performed.

To do that you type:

`python3 configuration.py`

It should go through the instructions for you.

After that it creates an empty file called "configured" that is how main.py knows whether its been run or not. Deleting this file will require configuration to be run again.

Changing the values in config.yaml will change the operations of the device on each main.py operation.

The files will be saved in Taphonomy-Rig/log/

### Testing:
If you want to test, there is a folder Taphonomy-Rig/basic/ which has blink scripts for the pins required for lifting and lowering.

The files are blink_22.py or blink_5.py which take in no input arguments.
The file blink.py requires a pin number and a duration 50% duty cycle always.
The scale file requires a offset and cal_factor as arguments.

## Pulling the data

It is simpler to make a tar(zipped) file when performing a group copy over to your machine. That can be done with this instruction from the ~ folder.

`tar -vcf myfile.tar ~/Taphonomy-Rig/log/*`

Then from a seperate terminal on your PC (Assuming Windows) you can run the line:

scp [username]@[IP]:~/[filename] [filename on your pc]

Example:

`scp justin@192.168.137.79:~/myfile.tar yemi.tar`

## First Time compressed

`sudo apt-get update; sudo apt-get install -y python3-pip git; sudo timedatectl set-timezone Africa/Johannesburg; git clone https://github.com/Montso/Taphonomy-Rig.git; cd Taphonomy-Rig/ sudo python3 -m pip install -r requirements.txt --break-system-packages`