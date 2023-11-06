import os

from flask import Blueprint, render_template
from .blueprints.api import api
from .blueprints.programs import programs

main = Blueprint("main", __name__)
main.register_blueprint(api, url_prefix='/program')
main.register_blueprint(programs, url_prefix='/api')

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
    program_files = [f for f in os.listdir(program_dir) if f.endswith('.py')]
    return render_template("modules/program.html", programs=program_files)


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
