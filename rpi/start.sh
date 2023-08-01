#!/bin/bash

export $(/usr/bin/dbus-launch)
/usr/bin/python3 /home/pi/rosa-master/rpi/ws_server.py --verbose
