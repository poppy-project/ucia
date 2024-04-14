from flask import Blueprint, jsonify, request, redirect, url_for, send_from_directory
import paho.mqtt.client as mqtt
import os
import random

camera = Blueprint('camera', __name__)

client_id = f'python-mqtt-{random.randint(0, 1000)}'
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()


@camera.route('/update_config', methods=['POST'])
def update_config():
    data = request.json
    mqtt_client.publish("vision/config", json.dumps(data))
    return jsonify({"status": "configuration updated"})

@camera.route('/get_image')
def get_image():
    try:
        print("test")
        # Assume image filename is 'camera.jpg' but adapt as necessary
        return send_from_directory('/tmp/rosa/images', 'camera.jpg', as_attachment=False)
    except FileNotFoundError:
        return "Image not found", 404

