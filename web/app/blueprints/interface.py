import subprocess
import os
import sys
import threading
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


    @interface.route('/execute', methods=['POST'])
    def execute_code():
        try:
            data = request.get_json()
            code = data.get('code')

            exec_thread = threading.Thread(target=exec, args=(code, globals()))
            exec_thread.start()

            return jsonify({'message': 'Code execution started'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

except ImportError as e:
    print(f"Error importing module 'manuel': {e}")