from ...remote_io import RemoteIO
from ..base_controller import BaseRobot
from .wheel import Wheel

class DynamicObject:
    pass

class RGBLed:
    def __init__(self, remote_io, id):
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

        if not all(isinstance(i, int) and 0 <= i <= 255 for i in (r, g, b)):
            raise ValueError("Each color component should be an integer between 0 and 255")

        self._r = r
        self._g = g
        self._b = b

        self._io.push_cmd({
            'leds': {
                self._id : [self._r, self._g, self._b]
            }
        })


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


        # self._left_led = LED(side='left', remote_io=self._io)
        # self._front_led = LED(side='center', remote_io=self._io)
        # self._right_led = LED(side='right', remote_io=self._io)

    @property
    def left_wheel(self):
        return self._left_wheel

    @property
    def right_wheel(self):
        return self._right_wheel
    
    @property
    def leds(self):
        return self._leds
   
#    @property
#     def left_led(self):
#         return self._left_led

#     @property
#     def front_led(self):
#         return self._front_led

#     @property
#     def right_led(self):
#         return self._right_led

#     @property
#     def camera(self):
#         return self._cam

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
