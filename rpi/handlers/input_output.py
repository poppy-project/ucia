import json
import time
from threading import Thread
from SimpleWebSocketServer import WebSocket

from settings import use_cam, line_center
from dbus_thymio import ThymioController

thymio_controller = ThymioController("./thympi.aesl")

class WsIOHandler(WebSocket):
    pub_period = 1.0 / 50.0

    def handleConnected(self):
        self._send_loop_running = True
        
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
        
        # TODO: Replace print with logger !
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
