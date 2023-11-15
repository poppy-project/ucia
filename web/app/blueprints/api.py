import subprocess
import os

from flask import Blueprint, jsonify, request

api = Blueprint('api', __name__)

@api.route('/update')
def update():
    """
    This endpoint attempts to update the local git repository by executing a 'git pull' command in the current working directory. 
    If the command is successful, a JSON response containing a success message and the command's output is returned. 
    If an error occurs during the execution of the command, a JSON response containing an error message is returned.
    
    :return: A JSON response containing either a success message and the command's output or an error message.
    :rtype: A Flask Response object with a JSON payload.
    """
    try:
        result = subprocess.run(['git', 'pull'], cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            raise Exception(f'Command failed: {result.stderr}')

        return jsonify({'message': 'Update successful', 'output': result.stdout}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def update_hostapd_conf(ssid, passphrase):
    conf_path = '/etc/hostapd/hostapd.conf'
    with open(conf_path, 'r') as file:
        lines = file.readlines()

    with open(conf_path, 'w') as file:
        for line in lines:
            if line.startswith('ssid='):
                file.write(f'ssid={ssid}\n')
            elif line.startswith('wpa_passphrase='):
                file.write(f'wpa_passphrase={passphrase}\n')
            else:
                file.write(line)

@api.route('/hotspot', methods=['POST'])
def update_hotspot():
    try:
        data = request.get_json()
        hotspot_name = data.get('hotspot_name')
        hotspot_password = data.get('hotspot_password')
        hotspot_enabled = data.get('hotspot_enabled')
        
        script_path = os.path.join(os.getcwd(), 'scripts', 'update_hostapd_conf.sh')
        subprocess.run([script_path, hotspot_name, hotspot_password], check=True)
            
        if hotspot_enabled:
            subprocess.run(['sudo', 'systemctl', 'restart', 'hostapd'])
            subprocess.run(['sudo', 'systemctl', 'stop', 'wpa_supplicant'])
        
        return jsonify({'message': 'Hotspot updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def update_wpa_supplicant_conf(ssid, passphrase):
    conf_path = '/etc/wpa_supplicant/wpa_supplicant.conf'
    with open(conf_path, 'w') as file:
        file.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
        file.write("update_config=1\n")
        file.write(f"network={{\n")
        file.write(f"    ssid=\"{ssid}\"\n")
        file.write(f"    psk=\"{passphrase}\"\n")
        file.write(f"}}\n")

@api.route('/wifi', methods=['POST'])
def update_wifi():
    try:
        data = request.get_json()
        wifi_ssid = data.get('wifi_ssid')
        wifi_password = data.get('wifi_password')
        wifi_enabled = data.get('wifi_enabled')

        update_wpa_supplicant_conf(wifi_ssid, wifi_password)
        
        if wifi_enabled:
            subprocess.run(['sudo', 'systemctl', 'restart', 'wpa_supplicant'])
            subprocess.run(['sudo', 'systemctl', 'stop', 'hostapd'])

        return jsonify({'message': 'Wi-Fi updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
