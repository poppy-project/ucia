import logging
import time

from tasks.thymio.follow_line_sensors import FollowLineSensors
from tasks.thymio.follow_line import FollowLine
from tasks.thymio.object_collector import ObjectCollector
from tasks.thymio.photographer import Photographer
from tasks.api import API

from manager.base import BaseManager
from controller.thymio.controller import ThymioController

class ThymioManager(BaseManager):
    current_mode = 0
    last_mode_change_time = 0  
    mode_change_delay = 0.5

    def __init__(self):
        self.controller = ThymioController()
        self.logger = logging.getLogger(__name__)
        
        self.api = API(self.controller)
                
        self.tasks = [
            ObjectCollector(self.controller), 
            FollowLine(self.controller), 
            FollowLineSensors(self.controller),
            Photographer(self.controller),
        ]

        self.num_modes = len(self.tasks)
        self.tasks[self.current_mode].init()


    def change_mode(self):
        current_time = time.time()

        if current_time - self.last_mode_change_time <  self.mode_change_delay:
            return
        
        button_top = bool(self.controller.get_state('button.forward')[0])
        button_bottom = bool(self.controller.get_state('button.backward')[0])
        button_left = bool(self.controller.get_state('button.left')[0])
        button_right = bool(self.controller.get_state('button.right')[0])
                
        if button_left or button_right or button_top or button_bottom:
            self.tasks[self.current_mode].close()
            previous_mode = self.current_mode
            self.last_mode_change_time = current_time     
            
        if button_left or button_top:
            self.current_mode = (self.current_mode + 1) % self.num_modes
            self.logger.info(f"Mode changed (UP) - Previous mode was {previous_mode}, new mode is {self.current_mode}.")
            self.tasks[self.current_mode].init()


        if button_right or button_bottom:
            self.current_mode = (self.current_mode - 1) % self.num_modes
            self.logger.info(f"Mode changed (BACK) - Previous mode was {previous_mode}, new mode is {self.current_mode}.")
            self.tasks[self.current_mode].init()


    def run(self):
        self.change_mode()

        self.tasks[self.current_mode].run()

    def close():
        pass