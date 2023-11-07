import logging

from controller.base import BaseController
from tasks.base import Task

from sockets.input_output import InputOuputServer
from sockets.camera import CameraServer
from sockets.webrtc import WebRTC
import asyncio
import threading


class API(Task):
    def __init__(self, controller: BaseController):
        self.controller = controller
        self.logger = logging.getLogger(__name__)

        # Création d'un thread pour la boucle d'événements asyncio.
        self.loop_thread = threading.Thread(target=self.start_asyncio_loop, daemon=True)
        self.loop_thread.start()

    def start_asyncio_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        self.input_output = InputOuputServer(self.controller)
        self.input_output.run()

        self.camera_server = CameraServer()
        self.camera_server.run()
        
        self.webrtc_server = WebRTC()
        self.webrtc_server.run()

        
        self.loop.run_forever()

    def run(self):
        self.logger.info("API")

    def close(self):
        # Arrêtez la boucle d'événements asyncio depuis le thread principal.
        self.loop.call_soon_threadsafe(self.loop.stop)

        # Attendez la fin du thread.
        self.loop_thread.join()

    def __exit__(self):
        self.close()
