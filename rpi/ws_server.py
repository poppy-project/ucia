import json
import time

import cv2 as cv

from PIL import Image
from io import BytesIO
from threading import Thread
from collections import deque

from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer


import io_controller as io
from line_tracking import get_line_center

from dbus_thymio import ThymioController

verbose = True
use_cam = [False]
line_center = [None]
thymio_controller = ThymioController("./thympi.aesl")

class WsIOHandler(WebSocket):
    pub_period = 1.0 / 50.0
    init = True

    # def __init__(self):
    #     super().__init__()
    #     self.thymio_controller = ThymioController("./thympi.aesl")

    def handleConnected(self):
        self._send_loop_running = True
        # if self.init:
        #     self.init_thymio_controller()
        # self.init = False
        def _send_loop():
            state_getter = self.stateGetter()
            last_state = next(state_getter)

            while self._send_loop_running:
                state = next(state_getter)
                if use_cam[0]:
                    state['line-center'] = line_center[0]

                last_state.update(state)

                # TODO: qu'est-ce qui declenche l'envoie du state ?
                #
                # Timer ?
                # REQ/REP ?
                #
                # Problematique : eviter les lags/buffer overflow en cas de latence reseau
                self.sendMessage(json.dumps(last_state))
                time.sleep(WsIOHandler.pub_period)

        self._sender = Thread(target=_send_loop)
        self._sender.start()

    def stateGetter(self):
        def _get(color):
            state = {
                'distance' : 0
            }

            return state

        while True:
            yield _get(color=True)

            for _ in range(19):
                yield _get(color=False)

    def handleMessage(self):
        cmd = json.loads(self.data)

        if verbose:
            print('Got cmd: {}'.format(cmd))

        if 'wheels' in cmd:
            wheels = cmd['wheels']
            left_speed = 0.0
            right_speed = 0.0

            if 'a' in wheels: 
                left_speed = wheels['a']

            if 'b' in wheels: 
                right_speed = wheels['b']

            thymio_controller.set_speed(left_speed, right_speed)

            for m in ('a', 'b'):
                if m in wheels:
                    if verbose:
                        print('Set motor {} speed to {}'.format(m, wheels[m]))

        if 'leds' in cmd:
            leds = cmd['leds']
            for side, led_id in (('left', 3), ('center', 2), ('right', 1)):
                if side in leds:
                    io.led_on(led_id) if leds[side] else io.led_off(led_id)

        if 'buzz' in cmd:
            duration = cmd['buzz']
            io.buzz(duration)

        if 'camera' in cmd and cmd['camera']:
            use_cam[0] = True

    def handleClose(self):
        for m in ('a', 'b'):
            io.set_motor_speed(m, 0)

        self._send_loop_running = False
        self._sender.join()

        use_cam[0] = False


ws = deque([], 1)
buff = deque([], 1)


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


def publish_loop():
    while True:
        if len(ws) and len(buff):
            ws[0].sendMessage(buff.pop())

        time.sleep(1.0 / 20)


class WsCamServer(WebSocket):
    def handleConnected(self):
        ws.append(self)

    def handleClose(self):
        ws.remove(self)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    io_server = SimpleWebSocketServer('', 1234, WsIOHandler)
    cam_server = SimpleWebSocketServer('', 5678, WsCamServer)

    if args.verbose:
        print('Server up and running.')

    video_loop = Thread(target=grab_frame_loop)
    video_loop.daemon = True
    video_loop.start()

    publish_t = Thread(target=publish_loop)
    publish_t.daemon = True
    publish_t.start()

    servers = [
        Thread(target=server.serveforever)
        for server in (io_server, cam_server)
    ]
    for server in servers:
        server.start()

    for server in servers:
        server.join()
