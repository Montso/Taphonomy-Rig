#!/usr/bin/env python3
import subprocess
import os, signal

def disconnect_ssh():
    while(1):
        try:
            out = subprocess.check_output(["pidof","ssh"])
            out = int(out.split()[0])
            print(out)
            if out:
                print("Killing Reverse SSH on process above")    
                os.kill(out, signal.SIGINT)
        except subprocess.CalledProcessError as e:
            print("Waiting for SSH connection")
            break
        
if __name__ == "__main__":
    disconnect_ssh()
