class Sound(object):
    def __init__(self, remote_io):
        self._io = remote_io

    def system(self, value):
        if not 0 <= value <= 7:
            return

        self._io.push_cmd({
            'sound': {
                'system' : value
            }
        })

    def frequency(self, hertz, ds):
        self._io.push_cmd({
            'sound': {
                'frequency' : [hertz, ds]
            }
        })

