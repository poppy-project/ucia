#!/bin/bash

# update_wpa_supplicant_conf.sh
# Usage: ./update_wpa_supplicant_conf.sh wifi_ssid wifi_password

WIFI_SSID=$1
WIFI_PASSWORD=$2
CONF_PATH="/etc/wpa_supplicant/wpa_supplicant.conf"

# Update the Wi-Fi SSID and password
cat > $CONF_PATH << EOF
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
    ssid="$WIFI_SSID"
    psk="$WIFI_PASSWORD"
}
EOF

echo "wpa_supplicant configuration updated with SSID: $WIFI_SSID"