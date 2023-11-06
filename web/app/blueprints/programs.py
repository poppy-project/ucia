import os
import json
from flask import Blueprint, jsonify, request


programs = Blueprint('programs', __name__)

@programs.route('/program/upload', methods=['POST'])
def upload_program():
    file = request.files['file']
    program_name = request.form['program_name']
    description = request.form['description']

    if file and file.filename.endswith('.py'):
        program_dir = os.path.expanduser("~/programs")
        file.save(os.path.join(program_dir, file.filename))
        
        # Update program.json
        data = {'programs': []}
        program_json_path = os.path.join(program_dir, 'program.json')
        if os.path.exists(program_json_path):
            with open(program_json_path, 'r') as f:
                data = json.load(f)
        data['programs'].append({
            "file_name": file.filename,
            "display_name": program_name,
            "description": description
        })
        
        with open(program_json_path, 'w') as f:
            json.dump(data, f, indent=4)
        return jsonify({"message": "Program uploaded successfully"}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400


@programs.route('/run', methods=['POST'])
def run():
    """
    Execute a specified program.
    :return: JSON response indicating success or failure.
    """
    data = request.get_json()
    program_name = data.get('program_name')

    # TODO: Implement the logic to run the program
    
    return jsonify({'message': f'Program {program_name} started successfully'}), 200


@programs.route('/kill', methods=['POST'])
def kill():
    """
    Stop a specified program.
    :return: JSON response indicating success or failure.
    """
    data = request.get_json()
    program_name = data.get('program_name')
    
    # TODO: Implement the logic to kill the program
    
    return jsonify({'message': f'Program {program_name} stopped successfully'}), 200
