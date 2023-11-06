from flask import Blueprint, jsonify, request
import os

programs = Blueprint('programs', __name__)

@programs.route('/upload', methods=['POST'])
def upload():
    try:
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(os.path.expanduser("~/programs"), uploaded_file.filename)
            uploaded_file.save(file_path)
        return redirect(url_for('main.program'))  # Redirigez vers la page des programmes
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
