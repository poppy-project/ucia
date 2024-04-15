from enum import Enum

class RobotState(Enum):
    API=0
    MODE=1

# TODO : Do we use it?
status: RobotState = RobotState.MODE

# TODO : Supress this
loading_model = True

def set_status(new_status: RobotState):
    global status
    status = new_status

import json
from pathlib import Path

class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.filepath = Path(__file__).parent / ("config_dev.json")
        # Configuration par défaut
        self.config_data = {
            "camera": {
                "brightness": 50,
                "saturation": 50,
                "contrast": 50,
                "exposure": 50
            }
        }
        self.load_config()

    def load_config(self):
        """Charge la configuration à partir du fichier JSON ou crée un nouveau fichier avec les valeurs par défaut."""
        if self.filepath.exists():
            with open(self.filepath, "r") as file:
                self.config_data = json.load(file)
        else:
            self.save_config()

    def save_config(self):
        """Sauvegarde la configuration actuelle dans le fichier JSON."""
        with open(self.filepath, "w") as file:
            json.dump(self.config_data, file, indent=4)

    def update_config(self, section, **kwargs):
        """Met à jour la configuration pour une section donnée avec les nouvelles valeurs fournies."""
        if section in self.config_data:
            self.config_data[section].update(kwargs)
            self.save_config()
        else:
            print(f"Section {section} not found in configuration.")

    def get_config(self, section=None):
        """Renvoie la configuration complète ou une section spécifique."""
        if section:
            return self.config_data.get(section, {})
        return self.config_data