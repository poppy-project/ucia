from __future__ import division

from rosa.vision import detect_objects


def look_around(rosa, speed=0.2):
    rosa.left_wheel.speed = speed
    rosa.right_wheel.speed = 0


def follow_cube(rosa, center, gain=0.3):
    dx, _ = center
    ls = gain * (0.5 * dx + 0.5)
    rs = gain * (0.5 * -dx + 0.5)

    rosa.left_wheel.speed = ls
    rosa.right_wheel.speed = rs

def sort_objects_by_center_x(objects):
    objects_sorted_by_center_x = sorted(objects, key=lambda obj: obj.center[0])
    return objects_sorted_by_center_x

def grab_object(rosa, img, labels = ['cube']):
    found_obj = sort_objects_by_center_x(detect_objects(img, render=True))

    cubes = [obj for obj in found_obj if obj.label in labels]
    if not cubes:  # We can't find a cube so we have to look around
        look_around(rosa)
    else:
        has_gathered_cube = any([c for c in cubes if c.center[1] > 770 and 610 < c.center[0] < 680])
        if has_gathered_cube:  # We got a cube, so we freeze!
            rosa.left_wheel.speed = 0
            rosa.right_wheel.speed = 0
            return True
        else:  # We haven't grabbed the cube yet so we move towards it
            # We arbitrarly decide that the first cube is our target.
            (x, y) = cubes[0].center
            height, width = 960, 1280
            target = (((x / width) * 2 - 1), -((y / height) * 2 - 1))

            follow_cube(rosa, target)
        return False