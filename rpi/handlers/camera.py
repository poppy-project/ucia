from collections import deque
from SimpleWebSocketServer import WebSocket
import time

import cv2 as cv
from PIL import Image
from io import BytesIO

from settings import use_cam, line_center
from line_tracking import get_line_center

# TODO: Rename and comment
ws = deque([], 1)
buff = deque([], 1)

#TODO: Comment
def grab_frame_loop():
    cap = cv.VideoCapture(0)

    while True:
        if not use_cam[0] and not len(ws):
            time.sleep(0.1)
            continue

        b, img = cap.read()
        if not b:
            continue

        with BytesIO() as bytes:
            pil_img = Image.fromarray(img)
            pil_img.save(bytes, 'jpeg')
            buff.append(bytes.getvalue())

        if use_cam[0]:
            center = get_line_center(img)
            if center is not None:
                center = (center[0] / img.shape[1],
                          center[1] / img.shape[0])
            line_center[0] = center

#TODO: Comment
def publish_loop():
    while True:
        if len(ws) and len(buff):
            ws[0].sendMessage(buff.pop())

        time.sleep(1.0 / 20)


# TODO: Comment
class WsCamServer(WebSocket):
    def handleConnected(self):
        ws.append(self)

    def handleClose(self):
        ws.remove(self)