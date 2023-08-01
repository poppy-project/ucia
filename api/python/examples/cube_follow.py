from __future__ import division

import cv2 as cv
import numpy as np

from rosa import Rosa
from rosa.vision import detect_objects


def look_around(rosa, speed=0.0):
    rosa.left_wheel.speed = speed
    rosa.right_wheel.speed = 0


def follow_cube(rosa, center, gain=0.25):
    dx, _ = center
    ls = gain * (0.5 * dx + 0.5)
    rs = gain * (0.5 * -dx + 0.5)

    rosa.left_wheel.speed = ls
    rosa.right_wheel.speed = rs

def adjust_value(val):
    # define the input and output ranges
    input_range = (50, 130)
    output_range = (0.1, 0.3)

    # calculate the proportion of val within the input range
    proportion = (val - input_range[0]) / (input_range[1] - input_range[0])

    # map this proportion to the output range
    result = output_range[0] + proportion * (output_range[1] - output_range[0])

    return result

if __name__ == '__main__':
    rosa = Rosa('rosa.local')

    while True:
        img = rosa.camera.last_frame

        if img is None:
            continue

        try:
            found_obj = detect_objects(img, render=True)
        except:
            print("[ERROR] Found object")

        cube = [obj for obj in found_obj if obj.label == 'cube']

        if not cube:  # We can't find a cube so we have to look around
            look_around(rosa, 0.1)
            # TODO : Make something visible such as LED
        else:
            # We arbitrarly decide that the first cube is our target.
            (x, y) = cube[0].center

            height, width = 256, 320
            # height, width = 256, 320
            
            center_x = width / 2
            center_y = height / 2
            

            relative_x = x - center_x
            relative_y = y - center_y
            
            left_speed = 0.0
            right_speed = 0.0

            pixel_space = 40
            
            if relative_x > pixel_space:
                print("right")
                left_speed = -adjust_value(relative_x)
                right_speed = 0.0
            elif relative_x < -pixel_space :
                print("LEFT")
                print(adjust_value(-relative_x))

                left_speed = adjust_value(-relative_x)
                right_speed = 0.0
            else:
                print("GO")
                if relative_y > 80:
                    print("Finish")
                    finish = True
                    left_speed = -0.0
                    right_speed = 0.0
                elif relative_y > 70:
                    print("TROP PRES")
                    left_speed = -0.2
                    right_speed = 0.2
                else:
                    print("TROP Loin")
                    left_speed = 0.2
                    right_speed = -0.2
            

            # # Adjust left and right wheel speeds based on the cube's position set the wheel speeds
            rosa.left_wheel.speed = left_speed
            rosa.right_wheel.speed = right_speed

        
        cv.imshow('get cube', img)
        cv.waitKey(1)
