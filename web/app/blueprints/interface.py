import subprocess
import os

from rosa import Rosa
from flask import Blueprint, jsonify, request

interface = Blueprint('interface', __name__)

@interface.route('/manuel')
def activeManuel():
    rosa = Rosa(rosa.local)
    
    try:
        data = request.get_json()
        dir = data.get('dir')
        speedL = data.get('speedL')
        speedR = data.get('speedR')      
 

        return jsonify({'message': 'Update successful'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@interface.route('/mode', methods=['POST'])
def activeMode():
    try:
        data = request.get_json()
        mode_name = data.get('name')
        
        script_path = f"/home/pi/rosa-master/rpi/mode/{mode_name}"
        subprocess.Popen(['/usr/bin/python3', script_path])
                
        return jsonify({'message': 'Mode ' + mode_name + ' activate'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500