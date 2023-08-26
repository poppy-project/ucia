class LED(object):
    def __init__(self, side, remote_io):
        self._io = remote_io
        self._side = side

        self._on = False

    def __repr__(self):
        return 'LED(side="{}", status="{}")'.format(
            self._side,
            'on' if self.is_on() else 'off'
        )

    def is_on(self):
        return self._on

    def on(self):
        self._set_val(True)

    def off(self):
        self._set_val(False)

    def toggle(self):
        self._set_val(not self.is_on())

    def _set_val(self, new_val):
        self._on = new_val
        self._io.set_led(self._side, self._on)
