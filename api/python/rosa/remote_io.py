import json
import time
import collections
import websocket as ws

from threading import Thread, Event, Lock


# See https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
def update_cmd(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update_cmd(d.get(k, {}), v)
        else:
            d[k] = v
    return d


class RemoteIO(object):
    def __init__(self, host):
        url = 'ws://{}:1234'.format(host)
        self.ws = ws.create_connection(url)

        self.last_state = {}

        self._poll_t = Thread(target=self._update_state)
        self._poll_t.daemon = True
        self._poll_t.start()

        self._cmd = {}
        self._cmd_lock = Lock()
        self._cmd_event = Event()
        self._push_t = Thread(target=self._push_cmd)
        self._push_t.daemon = True
        self._push_t.start()

        self._synced = Event()
        self._synced.wait()

    @property
    def connected(self):
        return self._push_t.is_alive() and self._poll_t.is_alive() and self._synced.is_set()

    def push_cmd(self, cmd):
        with self._cmd_lock:
            update_cmd(self._cmd, cmd)
            self._cmd_event.set()

    def _push_cmd(self):
        while True:
            self._cmd_event.wait()
            with self._cmd_lock:
                self.ws.send(json.dumps(self._cmd))
                self._cmd.clear()
                self._cmd_event.clear()
            time.sleep(1 / 50)

    def set_speed(self, motor, speed):
        self.push_cmd({
            'wheels': {
                motor: speed
            }
        })

    def set_led(self, led, val):
        self.push_cmd({
            'leds': {
                led: val
            }
        })

    def buzz(self, duration):
        self.push_cmd({'buzz': duration})

    def _update_state(self):
        while True:
            self.last_state.update(json.loads(self.ws.recv()))
            self._synced.set()
