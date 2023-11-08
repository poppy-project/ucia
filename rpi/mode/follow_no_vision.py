import cv2 as cv

from rosa import Rosa
from rosa.vision.line_tracking import get_line_center

import time

def set_speed(rosa, ls, rs):
    rosa.left_wheel.speed = ls
    rosa.right_wheel.speed = rs


if __name__ == '__main__':
    rosa = Rosa('rosa.local')

    while True:
        reflected = rosa.ground_reflected

        print(reflected)
        SPEED = 0.1
        
        threshold = 300
        if reflected[0] > threshold and reflected[1] < threshold:
            print("right")
            # set_speed(rosa,0,SPEED)
        elif reflected[0] < threshold and reflected[1] > threshold:
            print("left")
            # set_speed(rosa,SPEED, 0)
        elif reflected[0] < threshold and reflected[1] < threshold:
            print("straigh")
            # set_speed(rosa,SPEED, SPEED)
        else:
            print("lost")
        set_speed(rosa, 0, 0)
        time.sleep(0.016)
        