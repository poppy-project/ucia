import logging
import time
import subprocess

from tasks.api import API

from manager.base import BaseManager
from controller.thymio.controller import ThymioController
import settings 

class ThymioManager(BaseManager):
    current_mode = 0
    last_mode_change_time = 0  
    last_launch_change_time = 0

    mode_change_delay = 0.5
    launch_change_delay = 2
    current_process = None
    H = [20,0,0,0,0,0,0,0]
    first = True

    def __init__(self):
        self.controller = ThymioController()
        self.logger = logging.getLogger(__name__)
        
        self.api = API(self.controller)
                
        self.tasks = [
            "follow_no_vision.py",
            "follow_vision.py",
            "treasure.py"
        ]

        self.mode_colors = {
            "follow_no_vision.py": [0, 32, 32],  # Bleu clair
            "follow_vision.py": [0, 0, 32],       # Bleu foncé
            "treasure.py": [32, 32, 0]           # Jaune
        }

        self.num_modes = len(self.tasks)
        self.last_launch_change_time = time.time()

    def change_mode(self):
        current_time = time.time()

        if current_time - self.last_mode_change_time <  self.mode_change_delay:
            return
        
        button_left = bool(self.controller.get_state('button.left')[0])
        button_right = bool(self.controller.get_state('button.right')[0])
        button_top = bool(self.controller.get_state('button.forward')[0])
        button_bottom = bool(self.controller.get_state('button.backward')[0])

        button_center = bool(self.controller.get_state('button.center')[0])
                
        if button_left or button_right or button_top or button_bottom:            
            self.close()
            previous_mode = self.current_mode
            self.last_mode_change_time = current_time

        mode_script = self.tasks[self.current_mode]
        if mode_script in self.mode_colors:
            color = self.mode_colors[mode_script]
            self.controller.set_led("top", color)
        
        if button_left or button_top:
            self.current_mode = (self.current_mode + 1) % self.num_modes
            self.logger.info(f"Mode changed (UP) - Previous mode was {previous_mode}, new mode is {self.current_mode}.")

        if button_right or button_bottom:
            self.current_mode = (self.current_mode - 1) % self.num_modes
            self.logger.info(f"Mode changed (BACK) - Previous mode was {previous_mode}, new mode is {self.current_mode}.")

        if current_time - self.last_launch_change_time <  self.launch_change_delay:
            return

        if button_center:
            self.run_process()

    def run(self):
        self.logger.debug(f"Actual mode {settings.status}")
        # if settings.status != settings.RobotState.MODE:
            # return

        if settings.loading_model:
            self.controller.set_led("circle", self.H)
            self.H = self.H[-1:] + self.H[:-1]
        elif not(settings.loading_model) and self.first:
            self.H = [0] * 8
            self.controller.set_led("circle", self.H)
            self.first = False

        self.change_mode()

        time.sleep(0.016)

    
    def run_process(self):
        if self.current_process is not None:
            self.close()

        print()

        script_path = f"/home/pi/rosa-master/rpi/mode/{self.tasks[self.current_mode]}"
        self.current_process = subprocess.Popen(['/usr/bin/python3', script_path])


    def close(self):
        if self.current_process is not None:
            self.current_process.terminate()
            self.current_process.wait(timeout=10)
            self.current_process = None