import cv2 as cv

from rosa import Rosa
from rosa.vision.line_tracking import get_line_center

import time

base_speed = 0.1
turn_ratio = 0.9
THRESHOLD_DIFFERENCE = 50
following_left_edge = True

def set_speed(rosa, ls, rs):
    rosa.left_wheel.speed = ls
    rosa.right_wheel.speed = rs

def set_straight(rosa):
    set_speed(rosa, base_speed, base_speed)

def set_right(rosa):
    left_wheel_speed = base_speed * (1 + turn_ratio)
    right_wheel_speed = base_speed * (1 - turn_ratio)

    set_speed(rosa,left_wheel_speed, right_wheel_speed)

def set_left(rosa):
    left_wheel_speed = base_speed * (1 - turn_ratio)
    right_wheel_speed = base_speed * (1 + turn_ratio)
    print(left_wheel_speed)
    print(right_wheel_speed)
    
    set_speed(rosa,left_wheel_speed, right_wheel_speed)


if __name__ == '__main__':
    rosa = Rosa('rosa.local')

    while True:
        reflected = rosa.ground_reflected
        left_sensor = reflected[0]
        right_sensor = reflected[1]
        print(left_sensor)
        print(right_sensor)

        right_wheel_speed = 0
        left_wheel_speed = 0

        difference = abs(left_sensor - right_sensor)
        print(difference)
        # following_left_edge = left_sensor < right_sensor
        # print(following_left_edge)
        if difference < THRESHOLD_DIFFERENCE:
            if following_left_edge:
                print("right")
                set_right(rosa)
                # time.sleep(2)
                # set_speed(rosa, 0 , 0)
                # time.sleep(30)
                # left_wheel_speed = base_speed * (1 + turn_ratio)
                # right_wheel_speed = base_speed * (1 - turn_ratio)
            else:
                print("left")
                set_left(rosa)
                # left_wheel_speed = base_speed * (1 - turn_ratio)
                # right_wheel_speed = base_speed * (1 + turn_ratio)
        else:
            print("straigh")
            set_straight(rosa)
            # print(left_sensor)
            # print(right_sensor)
            following_left_edge = left_sensor > right_sensor
            print(following_left_edge)
            if following_left_edge:
                print("left edge")
            else:
                print("right_edge")
            # set_speed(rosa, left_wheel_speed, right_wheel_speed)
        # print(following_left_edge)
        # set_speed(rosa, 0, 0)
        # set_right(rosa)
        time.sleep(0.16)
        