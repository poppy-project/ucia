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
    "buttons": 8,
    "circle": 8,
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
        os.system("(/usr/bin/asebamedulla ser:name=Thymio-II &) && /bin/sleep 0.3")
        
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
    
    ### Controller part
        
    def fetch_current_state(self):
        pass

    # TODO: Remove a and b motor !
    def process_incoming_commands(self, cmd):
        if 'wheels' in cmd:
            wheels = cmd['wheels']
            self.set_speed(wheels.get('a', 0.0), wheels.get('b', 0.0))

        if 'leds' in cmd:
            leds = cmd['leds']
            for id, value in leds.items():
                self.logger.debug(f"id : {id}, value : {value}")
                self.set_led(id, value)

        if 'buzz' in cmd:
            duration = cmd['buzz']
            io.buzz(duration)


    def reset_robot_state(self):
        self.set_speed(0,0)


# def led_
    #     self.asebaNetwork.SendEventName(
    #         'leds.bottom.right',
    #         [0, self.ledState[0], 0]
    #     )

    # def mainLoop(self):
    #     # read and display acc sensors
    #     acc = self.asebaNetwork.GetVariable('thymio-II', 'acc')
    #     temperature = self.asebaNetwork.GetVariable('thymio-II', 'temperature')
    #     button_fd = self.asebaNetwork.GetVariable('thymio-II', 'button.forward')
    #     button_bw = self.asebaNetwork.GetVariable('thymio-II', 'button.backward')
    #     button_l = self.asebaNetwork.GetVariable('thymio-II', 'button.left')
    #     button_r = self.asebaNetwork.GetVariable('thymio-II', 'button.right')
    #     button_c = self.asebaNetwork.GetVariable('thymio-II', 'button.center')

    #     prox_horizontal = self.asebaNetwork.GetVariable('thymio-II', 'prox.horizontal')
    #     ground_ambiant = self.asebaNetwork.GetVariable('thymio-II', 'prox.ground.ambiant')
    #     ground_reflected = self.asebaNetwork.GetVariable('thymio-II', 'prox.ground.reflected')
    #     ground_delta = self.asebaNetwork.GetVariable('thymio-II', 'prox.ground.delta')
    #     mic_intensity = self.asebaNetwork.GetVariable('thymio-II', 'mic.intensity')

    #     # print the readed sensor values
    #     print(
    #         "Acc: {0:+3d}, {1:+3d}, {2:+3d} "
    #         "Temp: {3:3d} "
    #         "Button: f{4:1d}, r{5:1d}, b{6:1d}, l:{7:1d}, c:{8:1d} "
    #         "Horizontal: {9:4d}, {10:4d}, {11:4d}, {12:4d}, {13:4d}, {14:4d}, {15:4d}, "
    #         "Ground: [{16:3d}, {17:3d}, {18:3d}] | [{19:3d}, {20:3d}, {21:3d}], "
    #         "Mic: {22:3d}"
    #         "".format(
    #             *acc,
    #             *temperature,
    #             *button_fd,
    #             *button_r,
    #             *button_bw,
    #             *button_l,
    #             *button_c,
    #             *prox_horizontal,
    #             ground_ambiant[0],
    #             ground_reflected[0],
    #             ground_delta[0],
    #             ground_ambiant[1],
    #             ground_reflected[1],
    #             ground_delta[1],
    #             mic_intensity[0]
    #         )
    #     )

    #     # set programmatically some states on the thymio
    #     # optional you can specify reply- and error handler
    #     self.asebaNetwork.SendEventName(
    #         'motor.target',
    #         [0*acc[0], 16*acc[1]],
    #         reply_handler=self.dbusReply,
    #         error_handler=self.dbusError
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'leds.bottom.right',
    #         [0, self.ledState[0], 0]
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'leds.bottom.left',
    #         [0, 0, self.ledState[0]]
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'leds.temperature',
    #         [self.ledState[0], self.ledState[1]]
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'leds.circle',
    #         self.ledState
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'leds.prox.h',
    #         self.ledState
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'leds.prox.v',
    #         [self.ledState[0], self.ledState[2]]
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'leds.buttons',
    #         [self.ledState[0], self.ledState[1], self.ledState[2], self.ledState[3]]
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'leds.top',
    #         [self.ledState[0], self.ledState[1], self.ledState[2]]
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'leds.sound',
    #         [self.ledState[0]]
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'leds.rc',
    #         [self.ledState[4]]
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'mic.threshold',
    #         [200]
    #     )
    #     self.asebaNetwork.SendEventName(
    #         'sound.system',
    #         [self.counter % 8]
    #     )
    #     # self.asebaNetwork.SendEventName(
    #     #     'sound.play',
    #     #     [self.counter  % 8]
    #     # )
    #     # self.asebaNetwork.SendEventName(
    #     #     'sound.freq',
    #     #     [(self.counter * 10) % 3200, 1/60.0]
    #     # )

    #     # shift the ledState array
    #     # [1, 2, 4, 8, 16, 24, 32, 2] becomes [2, 1, 2, 4, 8, 16, 24, 32]
    #     self.ledState.append(self.ledState.pop(0))
    #     # increase the counter
    #     self.counter += 1
    #     # reschedule mainLoop
    #     self.run()
