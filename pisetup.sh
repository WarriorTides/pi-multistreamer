#!/bin/bash
# WE ARE USING RASPBERRYPI 4B with 64bit bookworm

if [[ "$(id -u)" != 0 ]]
  then echo "Please run as root"
  exit
fi


# Check if the PI is online
if ping -c 1 -W 2 1.1.1.1 > /dev/null; then
    echo "Wi-Fi is connected. Continuing..."
else
    echo "No Wi-Fi connection. Exiting."
    exit 1
fi

# Update and upgrade
apt update -y
apt upgrade -y

dpkg -l | grep ustreamer || apt install ustreamer -y

apt install python3-flask-cors -y
apt install python3-flask -y
#Make cams launch on startup
/usr/bin/python3 /home/pi/pi-multistreamer/cameras.py


crontab -l > crontab_new
echo "@reboot /usr/bin/python3 /home/pi/pi-multistreamer/server.py" >> crontab_new
crontab crontab_new
rm crontab_new


reboot now
