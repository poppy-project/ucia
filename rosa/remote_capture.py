import numpy as np
import websocket as ws

from PIL import Image
from io import BytesIO
from collections import deque
from threading import Thread


class RemoteCapture(object):
    def __init__(self, url):
        self.ws = ws.create_connection(url)
        self.buff = deque([], 1)

        self.video_loop_t = Thread(target=self.video_grab)
        self.video_loop_t.daemon = True
        self.video_loop_t.start()

    def read(self):
        if len(self.buff) == 0:
            return False, None

        jpeg_buff = self.buff.pop()
        with BytesIO(jpeg_buff) as f:
            pil_img = Image.open(f)
            img = np.asarray(pil_img)

        return True, img

    def video_grab(self):
        while True:
            img = self.ws.recv()
            self.buff.append(img)
