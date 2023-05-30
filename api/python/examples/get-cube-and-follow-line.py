from __future__ import division

import cv2 as cv

from rosa import Rosa
from rosa.vision import detect_objects, get_line_center


def look_around(rosa, speed=0.15):
    rosa.left_wheel.speed = speed
    rosa.right_wheel.speed = -speed


def follow_cube(rosa, center, gain=0.25):
    dx, _ = center
    ls = gain * (0.4 * dx + 0.6)
    rs = gain * (0.4 * -dx + 0.6)

    rosa.left_wheel.speed = ls
    rosa.right_wheel.speed = rs


def follow_line(rosa, center, gain=0.25, img_width=640):
    dx, _ = center
    dx = ((dx / img_width) - 0.5) * 2

    ls = gain * (0.5 * dx + 0.5)
    rs = gain * (0.5 * -dx + 0.5)

    rosa.left_wheel.speed = ls
    rosa.right_wheel.speed = rs


if __name__ == '__main__':
    rosa = Rosa('rosa.local')

    while True:
        img = rosa.camera.last_frame

        if img is None:
            continue

        found_obj = detect_objects(img, render=True)

        cubes = [obj for obj in found_obj if obj.label == 'cube']
        if not cubes:  # We can't find a cube so we have to look around
            look_around(rosa)
        else:
            has_gathered_cube = any([
                c for c in cubes
                if c.center[1] > 220 and 100 < c.center[0] < 200
            ])

            if has_gathered_cube:  # We got a cube, so we freeze!
                center = get_line_center(img, render=True)
                if center is None:
                    look_around(rosa)
                else:
                    follow_line(rosa, center)
            else:  # We haven't grabbed the cube yet so we move towards it
                # We arbitrarly decide that the first cube is our target.
                (x, y) = cubes[0].center
                height, width = 256, 320
                target = (((x / width) * 2 - 1), -((y / height) * 2 - 1))

                follow_cube(rosa, target)

        cv.imshow('get cube', img)
        cv.waitKey(1)
