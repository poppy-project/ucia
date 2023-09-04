import logging
import cv2 as cv

from controller.thymio.controller import ThymioController
from vision.camera import Camera
from tasks.base import Task

from vision import detect_objects


class ObjectCollector(Task):
    def __init__(self, controller: ThymioController):
        self.controller = controller
        self.logger = logging.getLogger(__name__)
        self.cam = Camera()

    def run(self):
        self.logger.info("OBJECT COLLECTOR")
        img = self.cam.grab_frame_loop()    

        if img is None:
            return

        found_obj = detect_objects(img, render=True)
        print(found_obj)
        # cv.imshow('Object Detection', img)
        # cv.waitKey(1)

        
    

    def close(self):
        pass