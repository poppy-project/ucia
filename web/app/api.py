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

@api.route('/hotspot', methods=['POST'])
def update_hotspot():
    """
    Handle a POST request to the '/hotspot' route.

    This endpoint updates the hotspot settings based on the data received in the request.
    The expected data format is JSON with keys 'hotspot_name' and 'hotspot_password'.

    :return: A JSON response indicating the success or failure of the update.
    :rtype: A Flask Response object with a JSON payload.
    """
    try:
        # Parse the JSON data from the request
        data = request.get_json()

        hotspot_name = data.get('hotspot_name')
        hotspot_password = data.get('hotspot_password')
        hostpot_enabled =  data.get('hotspot_enabled')

        # TODO: Update the hotspot settings with the received data
        print(f"Enabled ? {hostpot_enabled} - {hotspot_name} : {hotspot_password}")
        
        return jsonify({'message': 'Hotspot updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/wifi', methods=['POST'])
def update_wifi():
    """
    This endpoint updates the wifi settings based on the data received in the request.
    The expected data format is JSON with keys 'hotspot_name' and 'hotspot_password'.

    :return: A JSON response indicating the success or failure of the update.
    :rtype: A Flask Response object with a JSON payload.
    """
    try:
        # Parse the JSON data from the request
        data = request.get_json()
        wifi_ssid = data.get('wifi_ssid')
        wifi_password = data.get('wifi_password')
        wifi_enabled =  data.get('wifi_enabled')

        # TODO: Update the hotspot settings with the received data
        print(f"Enabled ? {wifi_enabled} - {wifi_ssid} : {wifi_password}")


        # TODO: Update the wifi settings with the received data

        return jsonify({'message': 'Wifi updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500