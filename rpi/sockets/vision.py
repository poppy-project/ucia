import json
import paho.mqtt.client as mqtt
from vision.camera import Camera

import random

class VisionServer:
    def __init__(self):
        client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("localhost", 1883, 60)
        self.client.subscribe("vision/config")
        self.client.loop_start()

        self.camera = Camera()
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully.")
        else:
            print("Connection failed with code %d." % rc)


        print("Connected with result code "+str(rc))

    def on_message(self, client, userdata, message):
        print("topic :", message.topic)
        # Update the camera configuration upon receiving a new message
        new_config = json.loads(message.payload)
        # self.config.update(new_config)
        # print("Updated configuration:", self.config)