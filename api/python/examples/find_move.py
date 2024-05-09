import time

from rosa import Rosa

def set_speed(rosa,left_speed, right_speed):
    rosa.left_wheel.speed = left_speed
    rosa.right_wheel.speed = right_speed

if __name__ == '__main__':
    # Connect to the robot using its hostname.
    rosa = Rosa('rosa.local',local_robot=False)

    print("turn left")
    set_speed(rosa, 0, 0.5)
    time.sleep(2)

    print("turn right")
    set_speed(rosa, 0.5, 0)
    time.sleep(2)

    print("go straight")
    set_speed(rosa, 0.5, 0.5)
    time.sleep(2)

    print("go behind")
    set_speed(rosa, -0.5, -0.5)
    time.sleep(2)