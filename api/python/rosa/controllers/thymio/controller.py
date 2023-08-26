from ...remote_io import RemoteIO
from ..base_controller import BaseRobot
from .wheel import Wheel
from .led import RGBLed, RBLed, LED, MultipleLed

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

        self._left_wheel = Wheel(id='b', side='left', remote_io=self._io)
        self._right_wheel = Wheel(id='a', side='right', remote_io=self._io, inverse=True)
        
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

        

    @property
    def left_wheel(self):
        return self._left_wheel

    @property
    def right_wheel(self):
        return self._right_wheel
    
    @property
    def leds(self):
        return self._leds
   
#     @property
#     def front_distance_sensors(self):
#         return ['front-left', 'front-center', 'front-right']

#     def get_front_distances(self):
#         """ Return distance from the front sensors (left, center, right). """
#         return np.array([self.get_distance(name) for name in self.front_distance_sensors])

#     @property
#     def ground_distance_sensors(self):
#         return [
#             'ground-front-left', 'ground-front-right',
#             'ground-rear-left', 'ground-rear-right',
#         ]

#     def get_ground_distances(self):
#         """ Return distance from the ground sensors (front left, front right, rear left, rear right). """
#         return np.array([self.get_distance(name) for name in self.ground_distance_sensors])

#     @property
#     def distance_sensors(self):
#         return self.front_distance_sensors + self.ground_distance_sensors

#     def get_distance(self, sensor):
#         """
#             Return distance from the given sensor.

#             See Rosa.distance_sensors for a list of all available sensors.
#         """
#         if sensor not in self.distance_sensors:
#             raise ValueError('sensor should be one of {}!'.format(self.distance_sensors))

#         return 255 - self._io.last_state['distance'][sensor]

#     def get_color(self):
#         """ Return RGBAmbient detected from the front center sensor. """
#         return self._io.last_state['color']['front-center']

#     def buzz(self, duration):
#         """ Trigger a buzz for duration (in sec). """
#         self._io.buzz(duration)
