import cv2 as cv

from rosa import Rosa
from rosa.vision import detect_objects


if __name__ == '__main__':
    rosa = Rosa('rosa.local')

    while True:
        img = rosa.camera.last_frame

        if img is None:
            continue

        found_obj = detect_objects(img, render=True)

        cv.imshow('Object Detection', img)
        cv.waitKey(1)
