import os
import threading
import dbus
import dbus.mainloop.glib
import sys
import os
import numpy as np
import logging

from controllers.base_controller import BaseRobot

LEDS = {
    "prox.h": 8,
    "prox.v": 2,
    "buttons": 4,
    "circle": 8,
    "top" : 3,
    "bottom.left": 3,
    "bottom.right": 3,
    "temperature": 2,
    "rc": 1,
    "sound": 1
}

class ThymioController(BaseRobot):
    logger = logging.getLogger(__name__)

    def __init__(self):
        # initialize asebamedulla in background and wait 0.3s to let asebamedulla startup
        os.system("(/usr/bin/asebamedulla ser:name=Thymio-II &) && /bin/sleep 3")
        
        # init the dbus main loop
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        # get stub of the aseba network
        bus = dbus.SessionBus()
        asebaNetworkObject = bus.get_object('ch.epfl.mobots.Aseba', '/')

        # prepare interface
        self.asebaNetwork = dbus.Interface(
            asebaNetworkObject,
            dbus_interface='ch.epfl.mobots.AsebaNetwork'
        )

        # Determine the directory containing the current script.
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to thympi.aesl within that directory.
        aesl_path = os.path.join(script_dir, "thympi.aesl")

        # load the file which is run on the thymio
        self.asebaNetwork.LoadScripts(
            aesl_path,
            reply_handler=self.dbusReply,
            error_handler=self.dbusError
        )
    
    def dbusReply(self):
        # dbus replys can be handled here.
        pass

    def dbusError(self, e):
        # dbus errors can be handled here.
        print('dbus error: %s' % str(e))

    def set_led(self, name, params):
        if name not in LEDS:
            self.logger.warning(f"LED '{name}' is not recognize.")
            return

        if LEDS[name] != len(params):
            self.logger.warning(f'Expected {LEDS[name]} parameters for {name}, but got {len(params)}')
            return
        
        self.logger.debug(f'Set led {name} with {params}')

        # Ensuring readiness by accessing a known variable ('acc') from the Thymio robot.
        # This step is required before sending an event.
        self.asebaNetwork.GetVariable('thymio-II', 'acc')
        
        # Sending the motor command
        self.asebaNetwork.SendEventName(
            'leds.' + name,
            params,
            reply_handler=self.dbusReply,
            error_handler=self.dbusError
        )


    def set_speed(self, left_motor, right_motor):
        self.logger.debug(f'Set left motor speed to {left_motor} and right motor speed to {right_motor}')

        # Ensuring readiness by accessing a known variable ('acc') from the Thymio robot.
        # This step is required before sending an event.
        self.asebaNetwork.GetVariable('thymio-II', 'acc')
        
        # Sending the motor command
        self.asebaNetwork.SendEventName(
            'motor.target',
            [500 * np.clip(left_motor, -1, 1), 500 * np.clip(right_motor, -1, 1)],
            reply_handler=self.dbusReply,
            error_handler=self.dbusError
        )
    
    def set_sound_system(self, value):
        self.logger.debug(f'Set sound system to {value}')

        if not 0 <= value <= 7:
            self.logger.warning('Value for sound system must be between 0 and 8')
            return

        # Ensuring readiness by accessing a known variable ('acc') from the Thymio robot.
        # This step is required before sending an event.
        self.asebaNetwork.GetVariable('thymio-II', 'acc')

        
        self.asebaNetwork.SendEventName(
            'sound.system',
            [value]
        )
    
    def set_frequency(self, value):    
        frequency_hz = value[0]
        duration_ds = value[1]

        self.logger.debug(f'Set sound frequency to {frequency_hz} Hz for a duration of {duration_ds} ds')

        # Ensuring readiness by accessing a known variable ('acc') from the Thymio robot.
        # This step is required before sending an event.
        self.asebaNetwork.GetVariable('thymio-II', 'acc')

        
        self.asebaNetwork.SendEventName(
            'sound.freq',
            value
        )

    
    ### Controller part
        
    def fetch_current_state(self):
        pass

    # TODO: Remove a and b motor !
    def process_incoming_commands(self, cmd):
        if 'wheels' in cmd:
            wheels = cmd['wheels']
            self.set_speed(wheels.get('left', 0.0), wheels.get('right', 0.0))

        if 'leds' in cmd:
            leds = cmd['leds']
            for id, value in leds.items():
                self.set_led(id, value)

        if 'sound' in cmd:
            sound = cmd['sound']
            if 'system' in sound:
                self.set_sound_system(sound['system'])
            elif 'frequency' in sound:
                self.set_frequency(sound['frequency'])


    def reset_robot_state(self):
        self.set_speed(0,0)
        for id, value in LEDS.items():
            self.set_led(id, [0] * value)
    
    def get_state(self):
        return {
            'acc' : self.asebaNetwork.GetVariable('thymio-II', 'acc'),
            'button' : {
                'forward' : self.asebaNetwork.GetVariable('thymio-II', 'button.forward'),
                'backward' : self.asebaNetwork.GetVariable('thymio-II', 'button.backward'),
                'left' : self.asebaNetwork.GetVariable('thymio-II', 'button.left'),
                'right' : self.asebaNetwork.GetVariable('thymio-II', 'button.right'),
                'center' : self.asebaNetwork.GetVariable('thymio-II', 'button.center')
            },
            'temperature' : self.asebaNetwork.GetVariable('thymio-II', 'temperature'),
            'prox_horizontal' : self.asebaNetwork.GetVariable('thymio-II', 'prox.horizontal'),
            'ground_ambiant' : self.asebaNetwork.GetVariable('thymio-II', 'prox.ground.ambiant'),
            'ground_reflected' : self.asebaNetwork.GetVariable('thymio-II', 'prox.ground.reflected'),
            'ground_delta' : self.asebaNetwork.GetVariable('thymio-II', 'prox.ground.delta'),
            'mic_intensity' : self.asebaNetwork.GetVariable('thymio-II', 'mic.intensity'),
        }