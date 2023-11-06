import os
import json
import time
import subprocess

from flask import Blueprint, jsonify, request, redirect, url_for

programs = Blueprint('programs', __name__)


@programs.route('/upload', methods=['POST'])
def upload_program():
    file = request.files['file']
    program_name = request.form['program_name']
    description = request.form['description']

    # Vérifie si le fichier est un fichier Python (.py)
    if file and allowed_file(file.filename):
        program_dir = os.path.expanduser("~/programs")
        timestamp = int(time.time())
        filename, ext = os.path.splitext(file.filename)
        unique_filename = f"{filename}_{timestamp}{ext}"
        file_path = os.path.join(program_dir, unique_filename)
        
        # Vérifie si le fichier n'existe pas déjà pour éviter d'écraser un fichier
        if not os.path.exists(file_path):
            file.save(file_path)
            
            # Met à jour program.json
            program_json_path = os.path.join(program_dir, 'program.json')
            data = {'programs': []}
            if os.path.exists(program_json_path):
                with open(program_json_path, 'r') as f:
                    data = json.load(f)
            data['programs'].append({
                "file_name": unique_filename,
                "display_name": program_name,
                "description": description
            })
            
            with open(program_json_path, 'w') as f:
                json.dump(data, f, indent=4)
            
            return redirect(url_for('main.program'))
        else:
            return jsonify({"error": "File already exists"}), 400
    else:
        return jsonify({"error": "Invalid file type"}), 400

def allowed_file(filename):
    return '.' in filename and filename.endswith('.py')

@programs.route('/run', methods=['POST'])
def run():
    """
    Execute a specified program.
    :return: JSON response indicating success or failure.
    """
    data = request.get_json()
    program_name = data.get('program_name')

    if not program_name:
        return jsonify({'error': 'No program name provided'}), 400

    # Assuming the programs are stored in a directory '~/programs'
    program_dir = os.path.expanduser("~/programs")
    program_path = os.path.join(program_dir, program_name)

    # Check if the file exists
    if not os.path.isfile(program_path):
        return jsonify({'error': 'Program not found'}), 404

    try:
        # Run the program in a new process
        # If you want to capture the output, you can add stdout=subprocess.PIPE, stderr=subprocess.PIPE
        subprocess.Popen(['python3', program_path])
        return jsonify({'message': f'Program {program_name} started successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
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

@programs.route('/delete/<filename>', methods=['POST'])
def delete_program(filename):
    program_dir = os.path.expanduser("~/programs")
    file_path = os.path.join(program_dir, filename)
    
    print(filename)
    # Supprimer le fichier physique
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        return jsonify({"error": "File not found"}), 404

    # Mettre à jour program.json
    program_json_path = os.path.join(program_dir, 'program.json')
    if os.path.exists(program_json_path):
        with open(program_json_path, 'r') as f:
            data = json.load(f)
        data['programs'] = [p for p in data['programs'] if p['file_name'] != filename]
        with open(program_json_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    return jsonify({"success": "Program deleted successfully"}), 200