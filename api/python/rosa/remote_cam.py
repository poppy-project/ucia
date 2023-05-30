import numpy as np
import websocket as ws

from collections import deque
from threading import Thread
from io import BytesIO

from PIL import Image


class Camera(object):
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

    def _video_grab(self):
        while True:
            img = self._ws.recv()
            self._buff.append(img)
