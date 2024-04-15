import numpy as np
import websocket as ws

from collections import deque
from threading import Thread
from io import BytesIO

from PIL import Image
import os
import json
import cv2 as cv

class CameraRemote(object):
    def __init__(self, host):
        url = 'ws://{}:5678'.format(host)
        self._ws = ws.create_connection(url)
        self._buff = deque([], 1)

        self._video_loop_t = Thread(target=self._video_grab)
        self._video_loop_t.daemon = True
        self._video_loop_t.start()

    def __repr__(self):
        h, w, _ = self.last_frame.shape
        return 'Camera(resolution="{}x{}")'.format(w, h)

    @property
    def last_frame(self):
        if len(self._buff) == 0:
            return None

        jpeg_buff = self._buff.pop()
        with BytesIO(jpeg_buff) as f:
            pil_img = Image.open(f)
            img = np.asarray(pil_img)

        return img.copy()

    @property
    def last_detection(self):
        return None

    @property
    def last_detection_frame():
        return None

    def _video_grab(self):
        while True:
            img = self._ws.recv()
            self._buff.append(img)

class VisualObject:
    def __init__(self, label, center, confidence):
        self.label = label
        self.center = center
        self.confidence = confidence

class IntegratedCamera:
    def __init__(self, image_dir="/tmp/rosa/images"):
        self.image_dir = image_dir

    @property
    def last_frame(self):
        # Load the last camera image from the file system
        camera_img_path = os.path.join(self.image_dir, 'camera.jpg')
        return cv.imread(camera_img_path)

    @property
    def last_detection_frame(self):
        # Load the last detected image from the file system
        detected_img_path = os.path.join(self.image_dir, 'detected_img.jpg')
        return cv.imread(detected_img_path)

    @property
    def last_detection(self):
        # Load the last detection data from the file system
        detected_data_path = os.path.join(self.image_dir, 'detected_data.json')
        try:
            if os.path.exists(detected_data_path):
                with open(detected_data_path, 'r') as f:
                    detections = json.load(f)
                    print("detection : ", detections)
                    visual_objects = [VisualObject(**d) for d in detections]
                print("visual", visual_objects)
                return visual_objects
        except:
            return []
        return []