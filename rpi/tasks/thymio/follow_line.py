import logging
from tasks.base import Task
from controller.thymio.controller import ThymioController
from vision.camera import Camera
import cv2 as cv

from vision.line_tracking import get_line_center

class FollowLine(Task):
    def __init__(self, controller: ThymioController):
        self.controller = controller
        self.logger = logging.getLogger(__name__)
        self.cam = Camera()
        self.init()
    
    def init(self):
        self.controller.set_led("top", [0, 32, 32])

    def look_around(self, speed=0.15):
        self.controller.set_speed(speed, -speed)

    def follow_line(self, center, gain=0.15, img_width=640):
        dx, _ = center
        dx = ((dx / img_width) - 0.5) * 2

        ls = gain * (0.4 * dx + 0.6)
        rs = gain * (0.4 * -dx + 0.6)

        self.controller.set_speed(ls, rs)

    def run(self):
        self.logger.info("FOLLOW LINE")
        img = self.cam.grab_frame_loop()    

        if img is None:
            return

        center = get_line_center(img, render=True)

        if center is None:
            self.look_around()
        else:
            self.follow_line(center)

        # cv.imshow('follow line', img)
        # cv.waitKey(1)
        
    def close(self):
        pass