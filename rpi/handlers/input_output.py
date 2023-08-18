import json
import time
import logging
from threading import Thread
from SimpleWebSocketServer import WebSocket

from settings import use_cam, line_center
from controllers.thymio.controller import ThymioController
from controllers.base_controller import BaseRobot

# TODO: Remove a and b motor !
# TODO: Don't handle robot state and controller.
class WsIOHandler(WebSocket):
    pub_period = 1.0 / 50.0
    logger = logging.getLogger(__name__)
    controller : BaseRobot = ThymioController()

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
        self.controller.process_incoming_commands(cmd)


        if 'camera' in cmd and cmd['camera']:
            use_cam[0] = True

    def handleClose(self):
        # TODO: Better message
        self.logger.debug('[Sender] Disconnect')
        
        self.controller.reset_robot_state()

        self._send_loop_running = False
        self._sender.join()

        use_cam[0] = False
