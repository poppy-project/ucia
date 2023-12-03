#!/bin/bash

sudo cp /etc/apt/sources.list /etc/apt/sources.list.backup

echo "deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi" | sudo tee /etc/apt/sources.list

sudo apt update

echo "DEBUG"

# sed -i 's/stable\/updates/stable-security\/updates/' /etc/apt/sources.list
# deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi
