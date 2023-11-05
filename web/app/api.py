import subprocess
import os

from flask import Blueprint, jsonify, request

api = Blueprint('api', __name__)

@api.route('/update')
def update():
    try:
        result = subprocess.run(['git', 'pull'], cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            raise Exception(f'Command failed: {result.stderr}')

        return jsonify({'message': 'Update successful', 'output': result.stdout}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

