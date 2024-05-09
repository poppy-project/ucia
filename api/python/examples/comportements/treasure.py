from __future__ import division

import cv2 as cv
import cv2
import time
from enum import Enum

from rosa import Rosa
from rosa.vision import detect_objects
import cv2.aruco as aruco

from treasure.aruco_nest import go_to_aruco, turn_behind
from treasure.leds import set_led_color

class StateTreasure(Enum):
    SEARCH_CUBE = 1
    GRAB_CUBE = 2
    PUT_CUBE_LINE = 3
    GO_BEHIND = 4

def stop(rosa):
    rosa.left_wheel.speed = 0
    rosa.right_wheel.speed = 0

def look_around(rosa, speed=0.2):
    rosa.left_wheel.speed = speed
    rosa.right_wheel.speed = 0


def follow_cube(rosa, center, gain=0.4):
    dx, _ = center
    ls = gain * (0.5 * dx + 0.5)
    rs = gain * (0.5 * -dx + 0.5)

    rosa.left_wheel.speed = ls
    rosa.right_wheel.speed = rs

if __name__ == '__main__':
    rosa = Rosa('rosa.local', local_robot=False)
    state = StateTreasure.SEARCH_CUBE
    timer = time.time()
    
    set_led_color(rosa, 'yellow')

    while True:
        img = rosa.camera.last_frame

        if img is None:
            continue
        #state = StateTreasure.PUT_CUBE_LINE
        
        if state == StateTreasure.PUT_CUBE_LINE:
            if go_to_aruco(rosa, img):
                state = StateTreasure.GO_BEHIND
                timer = time.time()
                set_led_color(rosa, 'purple')
            time.sleep(0.2)
        elif state == StateTreasure.SEARCH_CUBE:
            try:
                found_obj = detect_objects(img, render=True)
            except:
                continue
            cubes = [obj for obj in found_obj if obj.label == 'cube']

            if not cubes:  # We can't find a cube so we have to look around
                look_around(rosa)
            else:
                has_gathered_cube = any([c for c in cubes if c.center[1] > 220 and 100 < c.center[0] < 200])
                if has_gathered_cube:
                    state = StateTreasure.GRAB_CUBE
                    set_led_color(rosa, 'blue')
                    rosa.left_wheel.speed = 0
                    rosa.right_wheel.speed = 0
                    timer = time.time()
                else:
                    (x, y) = cubes[0].center
                    height, width = 256, 320
                    target = (((x / width) * 2 - 1), -((y / height) * 2 - 1))    
                    follow_cube(rosa, target)
                
        elif state == StateTreasure.GRAB_CUBE:
            if time.time() - timer > 3.0:
                rosa.left_wheel.speed = 0
                rosa.right_wheel.speed = 0
                state = StateTreasure.PUT_CUBE_LINE
                set_led_color(rosa, 'green')
            else:
                rosa.left_wheel.speed = 0.25
                rosa.right_wheel.speed = 0.25
        elif state == StateTreasure.GO_BEHIND:  
            if time.time() - timer < 3.0:
                turn_behind(rosa)
            else:
                timer = time.time()
                state = StateTreasure.SEARCH_CUBE
                set_led_color(rosa, 'yellow')

        try:
            cv.imshow('get cube', img)
            cv.waitKey(1)
        except:
            pass
