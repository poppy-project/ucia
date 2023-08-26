import numpy as np

def clamp_color(c):
    return int(np.clip(c, 0, 32))

# TODO: Can we set color alone.

class RGBLed(object):
    def __init__(self, id, remote_io):
        self._io = remote_io
        self._id = id
        self._r = 0
        self._g = 0
        self._b = 0
    
    @property
    def color(self):
        return (self._r, self._g, self._b)
    
    @color.setter
    def color(self, value): 
        if not isinstance(value, (list, tuple)) or len(value) != 3:
            raise ValueError("Color should be a tuple or list of 3 integers: (r, g, b)")

        r, g, b = value


        self._r = clamp_color(r)
        self._g = clamp_color(g)
        self._b = clamp_color(b)

        self._io.push_cmd({
            'leds': {
                self._id : [self._r, self._g, self._b]
            }
        })

class RBLed(object):
    def __init__(self, id, remote_io):
        self._io = remote_io
        self._id = id
        self._r = 0
        self._b = 0
    
    @property
    def color(self):
        return (self._r, self._b)
    
    @color.setter
    def color(self, value):
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            raise ValueError("Color should be a tuple or list of 2 integers: (r, b)")

        r, b = value


        self._r = clamp_color(r)
        self._b = clamp_color(b)

        self._io.push_cmd({
            'leds': {
                self._id : [self._r, self._b]
            }
        })

class LED:
    def __init__(self, id, remote_io):
        self._io = remote_io
        self._id = id
        self._value = 0

    @property
    def color(self):
        return self._value
    
    @color.setter
    def color(self, value):
        self._value = clamp_color(value)

        self._io.push_cmd({
            'leds': {
                self._id : [self._value]
            }
        })

class MultipleLed(object):
    def __init__(self, id, length, remote_io):
        self._io = remote_io
        self._id = id
        self._length = length
        self._value = [0] * length

    @property
    def color(self):
        return self._value
    
    @color.setter
    def color(self, value):
        if not isinstance(value, (list, tuple)) or len(value) != self._length:
            raise ValueError(f"Color should be a tuple or list of {self._length} integers")

        self._value = [clamp_color(v) for v in value]

        self._io.push_cmd({
            'leds': {
                self._id : self._value
            }
        })
