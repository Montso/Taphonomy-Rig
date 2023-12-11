#!/usr/bin/env python3
import subprocess

keyfile = "/home/pi/.ssh/id_rsa"
primary_port = "9093"
secondary_port = "9094"
username_ipaddress = "justin@165.232.32.20"

# checks if there is an existing ssh process running in the background:
def ssh_running():
    secondary_flag = 0
    try:	
        out = subprocess.check_output(["pidof","ssh"])
        print(out)
        if out:
            print("Reverse SSH on process above")    
            secondary_flag = 1
    except subprocess.CalledProcessError as e:
        print("Waiting for SSH connection")
    run_ssh(secondary_flag)
 
# runs the ssh reverse tunnel
def run_ssh(secondary_flag_in):
    try:
        if(secondary_flag_in):
            print("attempting secondary connection")
            ssh_command= "ssh -o ServerAliveInterval=30 -i %s -N -R %s:localhost:22 %s" % (keyfile, secondary_port, username_ipaddress)
        else:
            ssh_command= "ssh -o ServerAliveInterval=30 -i %s -N -R %s:localhost:22 %s" % (keyfile, primary_port, username_ipaddress)
        ssh_output = subprocess.check_output(ssh_command, shell=True)
    except subprocess.CalledProcessError as e:
        print("Reverse shell failed")

if __name__ == "__main__":
    ssh_running()
