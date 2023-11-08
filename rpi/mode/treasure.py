import logging
import cv2 as cv

from controller.thymio.controller import ThymioController
from vision.camera import Camera
from tasks.base import Task

from time import sleep
from vision import detect_objects


chosen = None
chosen_bonus = 0
_home_distance = 0.0
_scan_distance = 0.0
_scan_speed = 0.03
logger = logging.getLogger(__name__)

def set_speed(rosa, ls, rs):
    rosa.left_wheel.speed = ls
    rosa.right_wheel.speed = rs

def choose_object(rosa, threshold=0.4):
    """
    Choose an object according to policy.
    Here, the object with the highest confidence.
    """
    found = None
    try:
        found = desirable(rosa.camera.last_detection)
    except ValueError:
        logger.warn("COLLECTOR ignore exception in Yolo3 rectangle drawing!")
    if not found:
        return []
    object = sorted(found, key=lambda v: v.confidence)[0]
    if object.confidence < threshold:
        return []
    logger.info(
        f"COLLECTOR choosing {object.label} at {object.center} score {object.confidence}"
    )
    return object

def desirable(self, objects):
    """Decide whether we want this kind of object."""
    return [x for x in objects if x.label == "star"]

def scan(rosa):
    """Look around, turning slowly clockwise."""
    # self.logger.info(f"COLLECTOR scanning, dist {self._scan_distance}")
    if abs(_scan_distance) > 100:
        _scan_speed = -_scan_speed
    set_speed(rosa, _scan_speed, -_scan_speed * 0.2)
    _scan_distance += _scan_speed / 0.03 * 2

def stop(rosa):
    """Stop turning."""
    set_speed(rosa, 0, 0)

def track(rosa, object, multiplier=0.6):
    """
    Turn towards chosen object.
    Convert delta ±170 ~ ±45° ~ ± 900 ms at speed 0.25
    """
    heading = object.center[0] - 170
    speed = 0.25 if heading > 0 else -0.25
    duration = abs(heading / 170.0 * 0.900 * multiplier)
    logger.info(
        f"COLLECTOR tracking {object.label} object at heading {heading}"
    )
    set_speed(rosa, speed, -speed)
    sleep(duration)
    stop(rosa)

def is_close(object, multiplier=0.4, threshold=-10):
    """Do we think this object is close enough to grab?"""
    azimuth = (200 - object.center[0]) * multiplier
    decision = azimuth < threshold or _home_distance > 2
    logger.info(
        f"COLLECTOR is {object.label} at az {azimuth} ({_home_distance} from home) close? {'Yes' if decision else 'No'}"
    )
    return decision

def grab(rosa, object, backup=2.0):
    """Grab the object and bring it back home."""
    logger.info(
        f"COLLECTOR grab {object.label} then back up additional {backup}"
    )
    set_speed(rosa, 0.2, 0.2)
    sleep(2.4)
    set_speed(rosa,-0.25, 0.25)
    sleep(3.6)
    set_speed(rosa,0.20, 0.20)
    sleep(2.0 + backup)
    set_speed(rosa,-0.2, -0.2)
    sleep(1)
    set_speed(rosa,0.30, -0.30)
    sleep(3.0)
    set_speed(rosa, 0, 0)

def good_candidate(chosen_obj):
    """Remember whether chosen_obj and chosen agree about the object."""
    if chosen:
        if chosen and chosen.label == chosen.label:
            chosen_bonus += 1
            logger.info(
                f"COLLECTOR good {chosen.label} bonus {chosen_bonus}"
            )
        return True
    if chosen:
        logger.info(f"COLLECTOR lost {chosen.label}")
    chosen = None
    chosen_bonus = 0
    return False

if __name__ == '__main__':
    rosa = Rosa('rosa.local')
    while True:
        img = rosa.camera.last_frame
        if img is None:
            continue

        chosen = choose_object(rosa)
        
        if not good_candidate(chosen) or chosen_bonus < 0:
            # Scan clockwise
            scan(rosa)
            flush()
            continue
        
        if chosen.confidence > 0.7 or chosen_bonus > 2:
            logger.info(f"COLLECTOR high confidence for {chosen.label}")

            track(rosa, chosen)
            if is_close(chosen):
                grab(rosa, chosen, backup=_home_distance)
                flush()
            else:
                set_speed(rosa, 0.1, 0.1)
                # Polling interval imposes backup ~ 1200 ms @
                _home_distance += 0.3
        else:
            # Try to stabilize choice
            set_speed(rosa, 0.06, 0.06)
            chosen_bonus -= 1
            logger.info(
                f"COLLECTOR try to focus on {chosen.label}, "
                f"bonus now {chosen_bonus}"
            )

        sleep(0.016)