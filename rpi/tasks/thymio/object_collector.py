import logging
import cv2 as cv

from controller.thymio.controller import ThymioController
from vision.camera import Camera
from tasks.base import Task

from time import sleep
from vision import detect_objects


class ObjectCollector(Task):
    def __init__(self, controller: ThymioController):
        self.controller = controller
        self.logger = logging.getLogger(__name__)
        self.cam = Camera()
        self.chosen = None
        self.chosen_bonus = 0
        self._home_distance = 0.0
        self._scan_distance = 0.0
        self._scan_speed = 0.03

    def run(self):
        self.logger.info("OBJECT COLLECTOR")
        img = self.cam.grab_frame_loop()

        if img is None:
            return

        chosen = self.choose_object()

        if not self.good_candidate(chosen) or self.chosen_bonus < 0:
            # Scan clockwise
            self.scan()
            self.flush()
            return

        if chosen.confidence > 0.7 or self.chosen_bonus > 2:
            self.logger.info(f"COLLECTOR high confidence for {chosen.label}")

            self.track(chosen)
            if self.is_close(chosen):
                self.grab(chosen, backup=self._home_distance)
                self.flush()
            else:
                self.controller.set_speed(0.1, 0.1)
                # Polling interval imposes backup ~ 1200 ms @
                self._home_distance += 0.3
        else:
            # Try to stabilize choice
            self.controller.set_speed(0.06, 0.06)
            self.chosen_bonus -= 1
            self.logger.info(
                f"COLLECTOR try to focus on {chosen.label}, "
                f"bonus now {self.chosen_bonus}"
            )

    def close(self):
        pass

    def desirable(self, objects):
        """Decide whether we want this kind of object."""
        return [x for x in objects if x.label == "star" or x.label == "sphere"]

    def flush(self):
        """Reset chosen, flush image buffer."""
        self.logger.info(f"COLLECTOR flush buffers")
        self.chosen = None
        self.chosen_bonus = 0
        self._home_distance = 0.0
        for i in range(3):
            _ = self.cam.grab_frame_loop()
            sleep(0.2)

    def scan(self):
        """Look around, turning slowly clockwise."""
        # self.logger.info(f"COLLECTOR scanning, dist {self._scan_distance}")
        if abs(self._scan_distance) > 100:
            self._scan_speed = -self._scan_speed
        self.controller.set_speed(self._scan_speed, -self._scan_speed * 0.2)
        self._scan_distance += self._scan_speed / 0.03 * 2

    def stop(self):
        """Stop turning."""
        self.controller.set_speed(0, 0)

    def track(self, object, multiplier=0.6):
        """
        Turn towards chosen object.
        Convert delta ±170 ~ ±45° ~ ± 900 ms at speed 0.25
        """
        heading = object.center[0] - 170
        speed = 0.25 if heading > 0 else -0.25
        duration = abs(heading / 170.0 * 0.900 * multiplier)

        self.logger.info(
            f"COLLECTOR tracking {object.label} object at heading {heading}"
        )

        self.controller.set_speed(speed, -speed)
        sleep(duration)
        self.stop()

    def is_close(self, object, multiplier=0.4, threshold=-10):
        """Do we think this object is close enough to grab?"""
        azimuth = (200 - object.center[0]) * multiplier
        decision = azimuth < threshold or self._home_distance > 2
        self.logger.info(
            f"COLLECTOR is {object.label} at az {azimuth} ({self._home_distance} from home) close? {'Yes' if decision else 'No'}"
        )
        return decision

    def choose_object(self, threshold=0.4):
        """
        Choose an object according to policy.
        Here, the object with the highest confidence.
        """
        img = self.cam.grab_frame_loop()
        if img is None:
            return []

        found = None
        try:
            found = self.desirable(detect_objects(img, render=True))
        except ValueError:
            self.logger.warn("COLLECTOR ignore exception in Yolo3 rectangle drawing!")
        if not found:
            return []

        object = sorted(found, key=lambda v: v.confidence)[0]
        if object.confidence < threshold:
            return []

        self.logger.info(
            f"COLLECTOR choosing {object.label} at {object.center} score {object.confidence}"
        )
        return object

    def grab(self, object, backup=2.0):
        """Grab the object and bring it back home."""
        self.logger.info(
            f"COLLECTOR grab {object.label} then back up additional {backup}"
        )
        self.controller.set_speed(0.2, 0.2)
        sleep(2.4)
        self.controller.set_speed(-0.25, 0.25)
        sleep(3.6)
        self.controller.set_speed(0.20, 0.20)
        sleep(2.0 + backup)
        self.controller.set_speed(-0.2, -0.2)
        sleep(1)
        self.controller.set_speed(0.30, -0.30)
        sleep(3.0)
        self.controller.set_speed(0, 0)

    def good_candidate(self, chosen):
        """Remember whether chosen and self.chosen agree about the object."""
        if chosen:
            if self.chosen and self.chosen.label == self.chosen.label:
                self.chosen_bonus += 1
                self.logger.info(
                    f"COLLECTOR good {chosen.label} bonus {self.chosen_bonus}"
                )
            return True
        if self.chosen:
            self.logger.info(f"COLLECTOR lost {self.chosen.label}")
        self.chosen = None
        self.chosen_bonus = 0
        return False
