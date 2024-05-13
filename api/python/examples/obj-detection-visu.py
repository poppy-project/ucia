import cv2 as cv

from rosa import Rosa
from rosa.vision import detect_objects
import time

if __name__ == '__main__':
    rosa = Rosa('rosa.local', local_robot=False)

    while True:
        img = rosa.camera.last_frame

        rosa.left_wheel.speed = 0.0

        if img is None:
            continue

        found_obj = detect_objects(img, render=True)

        for i in found_obj:
            if i.label == "cube":
                print(i.label , " ", i.center)

        cv.imshow('Object Detection', img)
        cv.waitKey(1)
        time.sleep(0.16)
