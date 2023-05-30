import time
import numpy as np

from rosa import Rosa


if __name__ == '__main__':
    # Connect to the robot using its hostname.
    rosa = Rosa('rosa.local')

    pos = np.sin(np.linspace(0, 2 * np.pi, 1000))
    while True:
        for p in pos:
            rosa.left_wheel.speed = rosa.right_wheel.speed = p
            time.sleep(0.01)
