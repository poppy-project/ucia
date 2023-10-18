from flask import Flask
import os

from .routes import main  

def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=True)
    if config_name is None:
        app.config.from_object('instance.config.Config')
    else:
        app.config.from_object(config_name)
    
    
    app.register_blueprint(main)

    return app