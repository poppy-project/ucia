import os
import json

from flask import Blueprint, render_template
from .blueprints.api import api
from .blueprints.programs import programs
from .blueprints.camera import camera

main = Blueprint("main", __name__)
main.register_blueprint(api, url_prefix='/api')
main.register_blueprint(programs, url_prefix='/program')
main.register_blueprint(camera, url_prefix='/camera')
@main.context_processor
def inject_robot_config():
    return dict(version="0.1")


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/docs")
def docs():
    return render_template("modules/docs.html")


@main.route("/logs")
def logs():
    return render_template("modules/logs.html")


@main.route("/program")
def program():
    program_dir = os.path.expanduser("~/programs")

    # List all python files in the directory
    program_files = [f for f in os.listdir(program_dir) if f.endswith('.py')]
    program_data = {'programs': []}
    program_json_path = os.path.join(program_dir, 'program.json')
    
    # Load existing data from program.json if it exists
    if os.path.exists(program_json_path):
        with open(program_json_path, 'r') as f:
            program_data = json.load(f)

    # Merge the data from program.json and the directory listing
    for file in program_files:
        if not any(p['file_name'] == file for p in program_data['programs']):
            program_data['programs'].append({
                "file_name": file,
                "display_name": file.replace('.py', ''),
                "description": "Pas de description disponible."
            })
    
    return render_template("modules/program.html", programs=program_data['programs'])

@main.route("/settings")
def settings():
    return render_template("modules/settings.html")


@main.route("/terminal")
def terminal():
    return render_template("modules/terminal.html")


@main.route("/webcam")
def webcam():
    return render_template("modules/webcam.html")


@main.route("/shutdown")
def shutdown():
    return None


@main.route("/reboot")
def reboot():
    return None
