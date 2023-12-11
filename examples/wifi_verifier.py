#!/usr/bin/env python

import urllib.request
import os

def connected(host="https://google.com"):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

if __name__ == "__main__":
    if(not connected()):
        os.system("sudo systemctl daemon-reload")
        os.system("sudo systemctl restart dhcpcd")
    else:
        print("Internet Access Available")
