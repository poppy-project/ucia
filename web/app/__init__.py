from flask import Flask

from .routes import main  
from .api import api

def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=True)
    
    if config_name is None:
        app.config.from_object('instance.config.Config')
    else:
        app.config.from_object(config_name)
    
    
    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix='/api')

    return app