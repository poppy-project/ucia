#!/usr/bin/python3

import threading
import dbus
import dbus.mainloop.glib
import sys
import os


class ThymioController(object):
    def __init__(self, filename):
        # initialize asebamedulla in background and wait 0.3s to let
        # asebamedulla startup (!!bad habit to wait...)
        os.system("(asebamedulla ser:name=Thymio-II &) && sleep 5")
        
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

        # load the file which is run on the thymio
        self.asebaNetwork.LoadScripts(
            "./thympi.aesl",
            reply_handler=self.dbusReply,
            error_handler=self.dbusError
        )

        # initialize some variables which can be used in the main loop
        # to set thymio states
        # self.ledState = [1, 2, 4, 8, 16, 24, 32, 2]
        # self.counter = 0

    def stopAsebamedulla():
        # stop the asebamedulla process
        # !!dbus connection will fail after this call
        os.system("pkill -n asebamedulla")


    def dbusReply(self):
        # dbus replys can be handled here.
        # Currently ignoring
        pass

    def dbusError(self, e):
        # dbus errors can be handled here.
        # Currently only the error is logged. Maybe interrupt the mainloop here
        print('dbus error: %s' % str(e))

    def set_speed(self,left_motor, right_motor):
        acc = self.asebaNetwork.GetVariable('thymio-II', 'acc')

        print("send")
        self.asebaNetwork.SendEventName(
            'motor.target',
            [left_motor, right_motor],
            reply_handler=self.dbusReply,
            error_handler=self.dbusError
        )
        print("sent")

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
