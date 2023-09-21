import logging
import cv2 as cv

from controller.thymio.controller import ThymioController
from vision.camera import Camera
from tasks.base import Task

from vision import detect_objects


class Photographer(Task):
    def __init__(self, controller: ThymioController):
        self.controller = controller
        self.logger = logging.getLogger(__name__)
        self.cam = Camera()
        self.init()
  
    def init(self):
        self.controller.set_led("top", [0,32,0])

    def run(self):
        self.logger.info("PHOTOGRAPHER")
        img = self.cam.grab_frame_loop()    
        
        if img is None:
            return

        found_obj = detect_objects(img, render=True)

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