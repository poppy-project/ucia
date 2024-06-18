import subprocess
import os
import sys
import threading
from rosa import Rosa
from flask import Blueprint, jsonify, request,  send_from_directory

from ..controle.manuel import control

interface = Blueprint('interface', __name__)
dir_available = ['forward', 'backward', 'left', 'right', 'stop', 'buzz']

@interface.route('/manuel', methods=['GET'])
def activeManuel():
    try:
        dir = request.args.get('dir')
        speed = request.args.get('speed', default=0.2, type=float)
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




"""
@interface.route('/execute', methods=['POST'])
def execute_code():
    code = request.json.get('code', '')
    try:
        # Exécutez le code et capturez la sortie
        process = subprocess.Popen(
            ['python3', '-c', code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
            
        return jsonify({
            'stdout': stdout.decode('utf-8'),
            'stderr': stderr.decode('utf-8')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
"""    