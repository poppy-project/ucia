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
        self.init()

    def init(self):
        self.controller.set_led("top", [32, 32, 0])

    def look_around(self, speed=0.2):
        self.controller.set_speed(speed, 0)


    def follow_cube(self, center, gain=0.2):
        dx, _ = center
        ls = gain * (0.5 * dx + 0.5)
        rs = gain * (0.5 * -dx + 0.5)
        
        self.controller.set_speed(ls, rs)

    def run(self):
        self.logger.info("OBJECT COLLECTOR")
        img = self.cam.grab_frame_loop()

        if img is None:
            return

        found_obj = detect_objects(img, render=True)

        stars = [obj for obj in found_obj if obj.label == 'star']
        
        print(stars)
        
        if not stars:  # We can't find a cube so we have to look around
            self.look_around()
        else:
            has_gathered_star = any([
                c for c in stars
                if c.center[1] > 220 and 100 < c.center[0] < 200
            ])

            if has_gathered_star:  # We got a cube, so we freeze!
                self.logger.info("FINISH")
            else:  # We haven't grabbed the cube yet so we move towards it
                # We arbitrarly decide that the first cube is our target.
                self.logger.info("STAR FIND")

                (x, y) = stars[0].center
                height, width = 256, 320
                target = (((x / width) * 2 - 1), -((y / height) * 2 - 1))

                self.follow_cube(target)


        
    

    def close(self):
        pass