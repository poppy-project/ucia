import json
import websocket as ws


class RemoteController(object):
    def __init__(self, url):
        self.ws = ws.create_connection(url)

    def setup(self,
              AIN1, AIN2, PWMA,
              BIN1, BIN2, PWMB,
              STBY):
        self.ws.send(json.dumps({
            'setup': {
                'AIN1': AIN1, 'AIN2': AIN2, 'PWMA': PWMA,
                'BIN1': BIN1, 'BIN2': BIN2, 'PWMB': PWMB,
                'STBY': STBY
            }
        }))

    def set_speed(self, motor, speed):
        self.ws.send(json.dumps({
            'wheels': {
                motor: speed
            }
        }))
