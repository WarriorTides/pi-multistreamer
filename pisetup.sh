#!/bin/bash
# WE ARE USING RASPBERRYPI 4B with 64bit bookworm



if [[ "$(id -u)" != 0 ]]
  then echo "Please run as root"
  exit
fi


# Check if the PI is online
echo -e "GET http://google.com HTTP/1.0\n\n" | nc google.com 80 > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "Online"
else
    echo "Offline"
    exit
fi

# Update and upgrade
apt update -y
apt upgrade -y

dpkg -l | grep ustreamer || apt install ustreamer -y

 apt install python3-pip -y
 apt install python3-flask-cors -y
 apt install python3-flask -y
#Make cams launch on startup
crontab -l > crontab_new
echo "@reboot /usr/bin/python3 /home/pi/rang24-25/picamera/server.py" >> crontab_new
crontab crontab_new
rm crontab_new


reboot now