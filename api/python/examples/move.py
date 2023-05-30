import time

from rosa import Rosa


if __name__ == '__main__':
    # Connect to the robot using its hostname.
    rosa = Rosa('rosa.local')

    # The motor speed is normalized within range [-1, 1]
    # Positive speed means forward
    # Here, we will move forward at half max speed for 5s.
    rosa.left_wheel.speed = 0.5
    rosa.right_wheel.speed = 0.5
    time.sleep(5)

    # Here, we will move backward at max speed for 5s.
    rosa.left_wheel.speed = -1.0
    rosa.right_wheel.speed = -1.0
    time.sleep(5)

    # We can also spot turn
    rosa.left_wheel.speed = 0.25
    rosa.right_wheel.speed = -0.25
    time.sleep(3)

    # And in the other direction
    rosa.left_wheel.speed = -0.25
    rosa.right_wheel.speed = 0.25
    time.sleep(3)
