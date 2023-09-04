import logging

from controller.base import BaseController
from tasks.base import Task
# from sockets.input_output import InputOuputServer

class API(Task):
    def __init__(self, controller: BaseController):
        self.controller = controller
        self.logger = logging.getLogger(__name__)

        # self.input_output = InputOuputServer(self.controller)
        # self.input_output.run()

        # self.camera_server = CameraServer()
        # self.camera_server.run()

        # asyncio.get_event_loop().run_forever()

    def run(self):
        self.logger.info("API")

    def close(self):
        # self.input_output.close()
        pass