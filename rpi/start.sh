#!/bin/bash

/usr/bin/pkill -n asebamedulla
export $(/usr/bin/dbus-launch)
/usr/bin/python3 /home/pi/rosa-master/rpi/main.py --verbose
