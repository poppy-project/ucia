#!/bin/bash

# update_hostapd_conf.sh
# Usage: ./update_hostapd_conf.sh new_ssid new_passphrase

SSID=$1
PASSPHRASE=$2
CONF_PATH="/etc/hostapd/hostapd.conf"

# Update the SSID and passphrase directly in the configuration file
sudo sed -i "s/^ssid=.*/ssid=$SSID/" $CONF_PATH
sudo sed -i "s/^wpa_passphrase=.*/wpa_passphrase=$PASSPHRASE/" $CONF_PATH

echo "hostapd configuration updated with SSID: $SSID and passphrase"