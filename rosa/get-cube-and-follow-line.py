import cv2 as cv
import numpy as np

from PIL import Image
from keras.utils import get_file

from remote_capture import RemoteCapture
from remote_controller import RemoteController
from follow_utils import look_and_follow
from vision import get_black_line_center
from vision.yolo import YOLO


WEIGHTS = {
    'name': 'rosa-yolo-res256x320.h5',
    'origin': 'https://github.com/pollen-robotics/rosa/releases/download/0.1/rosa-yolo-res256x320.h5',
    'hash': 'fa9a254e4c00420430dd13d5a2eedda4068d71e6f44be475fa20120e6c62c90e',
}


def get_obj_center(yolo, yolo_res, looked_classes):
    boxes, scores, classes = yolo_res

    classes = np.array([yolo.class_names[c] for c in classes])
    selected = np.array([
        i for i, c in enumerate(classes)
        if c in looked_classes
    ], dtype='int64')
    boxes = boxes[selected]

    centers = [
        ((lx + 0.5 * (rx - lx)), (ly + 0.5 * (ry - ly)))
        for (ly, lx, ry, rx) in boxes
    ]

    width, height = pil_img.size
    centers = [
        (((x / width) * 2 - 1), -((y / height) * 2 - 1))
        for (x, y) in centers
    ]

    return centers


if __name__ == '__main__':
    cap = RemoteCapture('ws://rosa.local:5678')

    controller = RemoteController('ws://rosa.local:1234')
    controller.setup(
        AIN1=18, AIN2=17, PWMA=4,
        BIN1=24, BIN2=27, PWMB=22,
        STBY=23
    )

    model_path = get_file(
        fname=WEIGHTS['name'],
        origin=WEIGHTS['origin'],
        cache_subdir='rosa',
        file_hash=WEIGHTS['hash']
    )

    yolo = YOLO(
        model_path=model_path,
        anchors_path='./vision/yolo/tiny_yolo_anchors.txt',
        classes_path='./vision/yolo/classes.txt',
        model_image_size=(256, 320),
        score=0.2,
        iou=0.15,
    )

    while True:
        b, img = cap.read()
        if not b:
            continue

        img = cv.resize(img, (640, 480))
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        pil_img = Image.fromarray(img)
        pil_img, yolo_res = yolo.detect_image(pil_img)

        cubes = get_obj_center(yolo, yolo_res, ['cube'])
        gathered_cubes = [c for c in cubes if c[1] < -0.65]
        cubes_to_gather = [c for c in cubes if c[1] > -0.65]

        wrong_obj = get_obj_center(yolo, yolo_res, ['ball', 'star'])
        gathered_wrong_obj = [c for c in wrong_obj if c[1] < -0.7]

        if gathered_wrong_obj:  # Go backward
            controller.set_speed('a', -0.2)
            controller.set_speed('b', 0.2)
            continue

        if not len(gathered_cubes):
            target = cubes_to_gather[0] if len(cubes_to_gather) >= 1 else None
            look_and_follow(controller, target, look_speed=0.15, asserv_p=0.4)

            res_yolo = np.asarray(pil_img)
            res_yolo = cv.cvtColor(res_yolo, cv.COLOR_RGB2BGR)
            cv.imshow('Demo', res_yolo)
        else:
            _, center = get_black_line_center(
                img,
                band_center_y=300,
                band_width_ratio=1.0
            )
            look_and_follow(controller, center, look_speed=0.15, asserv_p=0.4)
            if center is not None:
                h, w, _ = img.shape
                x = int((center[0] + 1.0) * 0.5 * w)
                y = int((center[1] + 1.0) * 0.5 * h)
                cv.circle(img, (x, y), 10, (0, 0, 255), -1)
            cv.imshow('Demo', cv.cvtColor(img, cv.COLOR_BGR2RGB))

        cv.waitKey(1)
