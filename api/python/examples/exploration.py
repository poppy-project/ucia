import time
import numpy as np

from rosa import Rosa


"""
    Exploration mode.

    The robot will goes straightforward until it sees an obstacle or detect void below it.
    It will then do a random turn and keep going.

    The program runs forever until stops via Ctrl-c.
"""


cruise_speed = 0.15
gain = 0.25


def led_warning(rosa, duration, leds=('left_led', 'front_led', 'right_led')):
    start = time.time()

    while time.time() - start < duration:
        for led in leds:
            getattr(rosa, led).toggle()
            time.sleep(0.1)

    for led in leds:
        getattr(rosa, led).off()


def turn(rosa, angle, cw):
    print('Turning of {} degrees'.format(angle))
    speed = 0.006  # empirical degrees per second using +/- 0.15 as wheel speed

    rosa.left_wheel.speed = -0.15 if cw else 0.15
    rosa.right_wheel.speed = 0.15 if cw else -0.15
    led_warning(rosa, duration=speed * angle,
                leds=['right_led'] if cw else ['left_led'])

    rosa.left_wheel.speed = rosa.right_wheel.speed = 0


if __name__ == '__main__':
    rosa = Rosa('rosa.local')

    while True:
        obstacle_detected = np.any(rosa.get_front_distances() < 150)
        void_detected = np.any(rosa.get_ground_distances() > 0)

        if obstacle_detected or void_detected:
            # Back off for 1s to
            rosa.left_wheel.speed = -cruise_speed
            rosa.right_wheel.speed = -cruise_speed
            led_warning(rosa, duration=1)

            # Random turn within 45-135 degrees clockwise or counter clockwise
            turn(rosa, angle=np.random.randint(45, 135), cw=np.random.rand() > 0.5)

        rosa.left_wheel.speed = rosa.right_wheel.speed = cruise_speed
        time.sleep(1 / 50)
