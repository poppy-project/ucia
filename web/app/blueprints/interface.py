import subprocess
import os
import sys
from rosa import Rosa
from flask import Blueprint, jsonify, request

import sys
sys.path.append("/home/pi/rosa-master/rpi/mode/manuel/")

try:
    import manuel

    interface = Blueprint('interface', __name__)
    rosa = Rosa('rosa.local')  # Initialisez Rosa correctement
    dir_available = ['forward', 'backward', 'left', 'right', 'stop']

    @interface.route('/manuel', methods=['GET'])
    def activeManuel():
        try:
            dir = request.args.get('dir')
            speed = request.args.get('speed', default=0.2, type=float)

            if dir in dir_available:
                try:
                    manuel.control(rosa, dir, speed)
                    return jsonify({'message': 'Update successful'}), 200
                except ValueError as e:
                    return jsonify({'error': str(e)}), 500
            else:
                return jsonify({'error': 'Invalid direction'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @interface.route('/mode', methods=['POST']) #Route obsolete valide (migration des modes via le pc)
    def activeMode():
        try:
            data = request.get_json()
            mode_name = data.get('name')

            script_path = f"/home/pi/rosa-master/rpi/mode/{mode_name}"
            subprocess.Popen(['/usr/bin/python3', script_path])

            return jsonify({'message': 'Mode ' + mode_name + ' activate'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

except ImportError as e:
    print(f"Error importing module 'manuel': {e}")