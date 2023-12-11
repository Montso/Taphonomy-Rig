#! /bin/bash 
echo "Service Started"
while [ ! -c /dev/cdc-wdm0 ];
do
	sleep 1
	echo "waiting for device"
done;
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode='low-power'
sudo ip link set wwan0 down