# Pi HAT project

This code is to run on the Taphonomy rig. It includes code for the [Pi HAT project.](https://github.com/montso/Pi-HAT)

This document serves to provide enough information to get the device operational and provide enough information for one to feel competent in using the device.

You will need some familiarity with a Raspberry Pi as this has been designed for the Pi 0W 2.

We need to have the:
    required code + prerequisites
	calibrated the rig for the load cell using the configuration files
	Performed some accelerated Testing
	Setup cron to run at your desired time interval

To begin, you will need to have a Pi setup and have its terminal open.

## First time setup on the Pi is:

Running the following instructions will perform the setup for you.

`sudo apt-get update`

`sudo apt-get install -y python3-pip git`

`sudo timedatectl set-timezone Africa/Johannesburg`

`git clone https://github.com/Montso/Taphonomy-Rig.git`

`cd Taphonomy-Rig/`

### Then in Taphonomy-Rig/ folder

You just need to install the initial packages. That can be done with the following line.

`sudo python3 -m pip install -r requirements.txt --break-system-packages`

`rm Makefile`

`rm requirements.txt`

`rm default_config.yaml`

The full system should be operational in terms of function, but now its ready for Calibration

### Calibration

In order to trust the weights we are getting we do a linear best fit onto the numbers recieved on the load cell and some gold standard weights that we have which we will lift.

We are solving for y = mx + c. I have called the c the offset, and the m is the calibration factor. You can make use of the examples in the basic/ folder.

If you launch scale.py it will expect 2 additional arguements offset and cal_factor while we dont know them, we could just enter 0 and 1.

`cd basic`

`python3 scale.py 0 1`

Now we would need to lift and ensure we have that weight on the load cell.

#### Lifting within Calibration:

You can manually lift the system with the supplied winch in/out controller and its recommended when you are performing calibration. This is because I expect your terminal is displaying the values from the script scale.py.

Note: you could open a seperate terminal and make use of the other basic/ scripts for lifting and lowering.

Once you have values that you are satisfied with, we need to insert them into the config.yaml file.

If you are still in the basic/ from above, you would need to do

`cd ..`

Then you should be back in the Taphonomy-Rig/ folder and now using a simple text editor we can change the values

`nano config.yaml`

Within this file, you need to navigate to the cal_factor and offset and set them.

### Accelerated Testing

If you type

`python3 main.py`

It should fail saying its not confident configuration has been done. The program is looking for an additional file to ensure that its been done. To do that

`touch configured`

Now running main.py should perform a single lift. you can try again and it should be okay. I built in some functionality to perform some accelerated testing so that we dont need to wait weeks to gain trust in the overall rig.

We can change the measurement speeds and delays associated with lifting and perform multiple lifts back to back to see if everything seems stable over a much larger set of lifts.

To do this, you need to have looked at the test.yaml file and chosen your settings.

`nano test.yaml`

As a suggestion, I would make it measure less and not pause in key places, but stick to the original lifting and lowering times.

So for example

Before_Lift: 0.5

Stationary_pause: 0.5

While keeping the lift and lower times the same.

Then for Measurements

Default_readouts: 2

Default_averaging: 2

Once saved, running the line will perform 10 tests using the test.yaml file.

`python3 test.py 10 --config test.yaml`

To stop the code, ^C will kill the program.

If you are satisfied with the full operation, we need to move onto operating at the set time.

### Understanding cron

Cron is a program that is used to run pieces of code at specific points in the CPUs time. I make use of 2 cron events.

I reboot the device at 23:55 and I perform a lift 300 seconds after a reboot. I did it this way to ensure that it would do a lift 5 minutes after being plugged in for us to be confident if we ever chose to do that - RATHER than waiting till midnight :P

From the ~/Taphonomy-Rig/ folder, there is a setup file that copies the correct lines into crontab.

`crontab mycronjobs`

If you wanted to confirm the information,

`crontab -e`

will allow you to see the current information cron is using.

Finally we want to remove my file for cleanliness.

`rm mycronjobs`


### Basic Folder and Testing:
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

`scp justin@192.168.137.79:~/myfile.tar kris.tar`

## First Time compressed

`sudo apt-get update; sudo apt-get install -y python3-pip git; sudo timedatectl set-timezone Africa/Johannesburg; git clone https://github.com/Montso/Taphonomy-Rig.git; cd Taphonomy-Rig/; sudo python3 -m pip install -r requirements.txt --break-system-packages; mv ~/Taphonomy-Rig/.git_hooks_post-merge ~/Taphonomy-Rig/.git/hooks/post-merge; chmod +x ~/Taphonomy-Rig/.git/hooks/post-merge; crontab mycronjobs; mkdir log; rm mycronjobs; rm Makefile; rm requirements.txt; rm default_config.yaml; rm power.py; rm relay.py; rm scale.py; rm .git_hooks_post-merge'

## Fun fiddles

This is to get the version number and hash appearing correctly in the config file. To do this, I have made a file which needs to be moved into the hidden git folder with the correct name. The line below will facilitate this.

`mv ~/Taphonomy-Rig/.git_hooks_post-merge ~/Taphonomy-Rig/.git/hooks/post-merge`

Following that, we need to make it executable with the following line.

`chmod +x ~/Taphonomy-Rig/.git/hooks/post-merge`

In that script it will run the .sh file update-version which we also need to make executable. That is given below.

`chmod +x ~/Taphonomy-Rig/update-version.sh`

Then finally, this gets the information that we want, and makes use of a python file [update_version.py] to insert it correctly into the config.yaml file.

This will resolve it for tonight.....


`rm scale.py`

`rm .git_hooks_post-merge`

`rm power.py`
`rm relay.py`
