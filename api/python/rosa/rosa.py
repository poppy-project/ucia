import numpy as np

from .remote_io import RemoteIO
from .remote_cam import Camera
from .controllers.thymio.controller import ThymioRosa

class Rosa(object):
    # TODO : Make robot changed !
    def __init__(self, host):
        """ Connects to the robot.

            Host is a string representing the robot address. Can be "rosa.local" when using ZeroConf or directly the IP address such as "192.168.0.45".
        """
        self.robot = ThymioRosa(host=host)

        self._cam = Camera(host)
    
    def __getattr__(self, attr):
        """
        This method is called when the requested attribute is not found.
        We delegate the lookup to the robot object.
        """
        return getattr(self.robot, attr)

    # TODO: Add robot repr here
    def __repr__(self):
        return 'RosaClient(host="{}", connected={})'.format(self._host, self._io.connected)

 