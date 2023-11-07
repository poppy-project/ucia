import logging
import cv2 as cv

from controller.thymio.controller import ThymioController
from vision.camera import Camera
from tasks.base import Task

class Photographer(Task):
    def __init__(self, controller: ThymioController):
        self.controller = controller
        self.logger = logging.getLogger(__name__)
        self.cam = Camera()
        self.controller.set_led("top", [0,32,0])

    def run(self):
        self.logger.debug("PHOTOGRAPHER")
        found_obj = self.cam.grab_detected_data()    
        
        if found_obj is None:
            return

        if found_obj:
            obj = found_obj[0]
            label = obj.label
        
            if label == "cube":
                self.controller.set_led("bottom.left", [32,0,0])
                self.controller.set_led("bottom.right", [32,0,0])
            elif label == "star":
                self.controller.set_led("bottom.left", [0,0,32])
                self.controller.set_led("bottom.right", [0,0,32])
            elif label == "ball":
                self.controller.set_led("bottom.left", [32,0,32])
                self.controller.set_led("bottom.right", [32,0,32])
            else:
                pass


    def close(self):
        pass