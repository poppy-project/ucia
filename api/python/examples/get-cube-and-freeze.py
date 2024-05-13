from __future__ import division

import cv2 as cv

from rosa import Rosa
from rosa.vision import detect_objects


def look_around(rosa, speed=0.2):
    rosa.left_wheel.speed = speed
    rosa.right_wheel.speed = 0


def follow_cube(rosa, center, gain=0.25):
    dx, _ = center
    ls = gain * (0.5 * dx + 0.5)
    rs = gain * (0.5 * -dx + 0.5)

    rosa.left_wheel.speed = ls
    rosa.right_wheel.speed = rs

def sort_objects_by_center_x(objects):
    objects_sorted_by_center_x = sorted(objects, key=lambda obj: obj.center[0])
    return objects_sorted_by_center_x

def grab_object(rosa, img, label = 'cube'):
    found_obj = sort_objects_by_center_x(detect_objects(img, render=True))

    cubes = [obj for obj in found_obj if obj.label == label]
    if not cubes:  # We can't find a cube so we have to look around
        look_around(rosa)
    else:
        has_gathered_cube = any([c for c in cubes if c.center[1] > 600 and 600 < c.center[0] < 700])
        if has_gathered_cube:  # We got a cube, so we freeze!
            rosa.left_wheel.speed = 0
            rosa.right_wheel.speed = 0
            return True
        else:  # We haven't grabbed the cube yet so we move towards it
            # We arbitrarly decide that the first cube is our target.
            (x, y) = cubes[0].center
            height, width = 1280, 960
            target = (((x / width) * 2 - 1), -((y / height) * 2 - 1))

            follow_cube(rosa, target)
        return False

if __name__ == '__main__':
    rosa = Rosa('rosa.local', local_robot=False)

    while True:
        img = rosa.camera.last_frame

        if img is None:
            continue

        print(grab_object(rosa, img))

        cv.imshow('get cube', img)
        cv.waitKey(1)
