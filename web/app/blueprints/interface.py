import subprocess
import os
import sys
import threading
from rosa import Rosa
from flask import Blueprint, jsonify, request,  send_from_directory

from ..controle.manuel import control, rosa, define_rosa, forward, backward, turn_left, turn_right, stop, active_led, get_ground_value, get_distance_value

interface = Blueprint('interface', __name__)
dir_available = ['forward', 'backward', 'left', 'right', 'stop']

@interface.route('/manuel', methods=['GET'])
def activeManuel():
    try:
        dir = request.args.get("dir")
        speed = request.args.get("speed", default=0.2, type=float)
        if not dir or not speed:
            return jsonify({'error': 'Missing parameters'}), 400
        if dir in dir_available:
            try:
                control(dir, speed)
                return jsonify({'message': 'Update successful'}), 200
            except ValueError as e:
                return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': 'Invalid direction'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@interface.route('/sensor_values')
def sensor_values():
    valueGL = get_ground_value("left")
    valueGR = get_ground_value("right")
    valueAv1 = get_distance_value(4)
    valueAv2 = get_distance_value(3)
    valueAv3 = get_distance_value(2)
    valueAv4 = get_distance_value(1)
    valueAv5 = get_distance_value(0)
    valueAr1 = get_distance_value(5)
    valueAr2 = get_distance_value(6)
    
    return jsonify({"GL": str(valueGL),
                    "GR": str(valueGR),
                    "Av1": str(valueAv1),
                    "Av2": str(valueAv2),
                    "Av3": str(valueAv3),
                    "Av4": str(valueAv4),
                    "Av5": str(valueAv5),
                    "Ar1": str(valueAr1),
                    "Ar2": str(valueAr2)}
                   )


@interface.route('/execute', methods=['POST'])
def execute_code():
    code = request.json.get('code', '')
    try:
        # Créez le fichier de contexte
        context_code = """
        
from time import sleep
from app.controle.manuel import control, rosa, define_rosa, forward, backward, turn_left, turn_right, stop, active_led, get_ground_value, get_distance_value

{}
        """.format(code)

        # Écrivez le code de contexte dans un fichier temporaire
        with open('context_code.py', 'w') as f:
            f.write(context_code)
        
        # Exécutez le fichier de contexte et capturez la sortie
        process = subprocess.Popen(
            ['python3', 'context_code.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()

        # Supprimez le fichier temporaire après l'exécution
        os.remove('context_code.py')
            
        return jsonify({
            'stdout': stdout.decode('utf-8'),
            'stderr': stderr.decode('utf-8')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500