from ...remote_io import RemoteIO
from ..base_controller import BaseRobot
from .wheel import Wheel
from .led import RGBLed, RBLed, LED, MultipleLed
from .sound import Sound

class DynamicObject:
    pass

class ThymioRosa(BaseRobot):
    def __init__(self, host):
        """
        Connects to the robot.

        Host is a string representing the robot address. Can be "rosa.local" when using ZeroConf or directly the IP address such as "192.168.0.45".
        """
        self._io = RemoteIO(host)
        self._host = host

        # Wheel
        self._left_wheel = Wheel(id='left', side='left', remote_io=self._io)
        self._right_wheel = Wheel(id='right', side='right', remote_io=self._io, inverse=True)
        
        # LEDS
        self._leds = DynamicObject()
        self._leds.bottom = DynamicObject()
        self._leds.bottom.left = RGBLed(id='bottom.left', remote_io=self._io)
        self._leds.bottom.right = RGBLed(id='bottom.right', remote_io=self._io)

        self._leds.top = RGBLed(id='top', remote_io=self._io)

        self._leds.temperature = RBLed(id='temperature', remote_io=self._io)

        self._leds.rc = LED(id='rc', remote_io=self._io)
        
        self._leds.sound = LED(id='sound', remote_io=self._io)

        self._leds.prox = DynamicObject()
        self._leds.prox.h = MultipleLed(id='prox.h', remote_io=self._io, length=8)
        self._leds.prox.v = MultipleLed(id='prox.v', remote_io=self._io, length=2)

        self._leds.buttons = MultipleLed(id='buttons', remote_io=self._io, length=4)
                
        self._leds.circle = MultipleLed(id='circle', remote_io=self._io, length=8)

        # SOUND
        self._sound = Sound(remote_io=self._io)

    @property
    def left_wheel(self):
        return self._left_wheel

    @property
    def right_wheel(self):
        return self._right_wheel
    
    @property
    def leds(self):
        return self._leds
    
    @property
    def sound(self):
        return self._sound
    
    @property
    def acc(self):
        data = self._io.last_state['acc']
        return data

    @property
    def button_forward(self):
        return bool(self._io.last_state['button']['forward'][0])

    @property
    def button_backward(self):
        return bool(self._io.last_state['button']['backward'][0])

    @property
    def button_left(self):
        return bool(self._io.last_state['button']['left'][0])

    @property
    def button_right(self):
        return bool(self._io.last_state['button']['right'][0])

    @property
    def button_center(self):
        return bool(self._io.last_state['button']['center'][0])

    @property
    def temperature(self):
        return self._io.last_state['temperature'][0]

    @property
    def prox_horizontal(self):
        data = self._io.last_state['prox_horizontal']
        return data

    @property
    def ground_ambiant(self):
        data = self._io.last_state['ground_ambiant']
        return data

    @property
    def ground_reflected(self):
        data = self._io.last_state['ground_reflected']
        return data

    @property
    def ground_delta(self):
        data = self._io.last_state['ground_delta']
        return data

    @property
    def mic_intensity(self):
        return self._io.last_state['mic_intensity'][0]