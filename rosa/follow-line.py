import cv2 as cv

from remote_controller import RemoteController
from remote_capture import RemoteCapture
from follow_utils import look_and_follow
from vision import get_black_line_center


if __name__ == '__main__':
    controller = RemoteController('ws://rosa.local:1234')

    controller.setup(
        AIN1=18, AIN2=17, PWMA=4,
        BIN1=24, BIN2=27, PWMB=22,
        STBY=23
    )

    cap = RemoteCapture('ws://rosa.local:5678')

    try:
        while True:
            b, img = cap.read()
            if not b:
                continue

            _, center = get_black_line_center(
                img,
                band_center_y=300,
                band_width_ratio=1.0
            )

            if center is not None:
                h, w, _ = img.shape
                x = int((center[0] + 1.0) * 0.5 * w)
                y = int((center[1] + 1.0) * 0.5 * h)
                cv.circle(img, (x, y), 10, (0, 0, 255), -1)

            look_and_follow(controller, center, look_speed=0.2, asserv_p=0.4)

            cv.imshow('Follow black line', img)
            cv.waitKey(1)

    except KeyboardInterrupt:
        controller.set_speed('a', 0)
        controller.set_speed('b', 0)
