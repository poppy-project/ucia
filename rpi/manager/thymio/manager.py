import logging
import time

from manager.base import BaseManager
from enum import Enum, auto

from controller.thymio.controller import ThymioController

class RobotMode(Enum):
    TREASURE_HUNTER = 0
    LINE_FOLLOWER = 1
    API = 2


class ThymioManager(BaseManager):
    current_mode = RobotMode.API
    last_mode_change_time = 0  
    mode_change_delay = 0.5

    def __init__(self):
        self.controller = ThymioController()
        self.logger = logging.getLogger(__name__)

    def change_mode(self):
        current_time = time.time()

        if current_time - self.last_mode_change_time <  self.mode_change_delay:
            self.logger.debug("Mode change attempt ignored, waiting for delay to pass.")
            return
        
        button_left = bool(self.controller.get_state('button.left')[0])
        button_right = bool(self.controller.get_state('button.right')[0])
        
        enum_length = len(list(RobotMode))
        
        if button_left or button_right:
            previous_mode = self.current_mode
            self.last_mode_change_time = current_time     
        
        if button_left:
            self.current_mode = RobotMode((self.current_mode.value + 1) % enum_length)
            self.logger.info(f"Mode changed (UP) - Previous mode was {previous_mode}, new mode is {self.current_mode}.")

        if button_right:
            self.current_mode = RobotMode((self.current_mode.value - 1) % enum_length)
            self.logger.info(f"Mode changed (BACK) - Previous mode was {previous_mode}, new mode is {self.current_mode}.")

    def run(self):
        self.change_mode()

        if self.current_mode == RobotMode.TREASURE_HUNTER:
            self.logger.debug("The robot is in treasure hunter mode.")
        elif self.current_mode == RobotMode.LINE_FOLLOWER:
            self.logger.debug("The robot is in line follower mode.")
        elif self.current_mode == RobotMode.API:
            self.logger.debug("The robot is in API mode.")
        else:
            self.logger.debug("Unknown mode.")

    def close():
        pass