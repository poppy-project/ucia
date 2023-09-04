import logging
from tasks.base import Task
from controller.thymio.controller import ThymioController

class FollowLine(Task):
    def __init__(self, controller: ThymioController):
        self.controller = controller
        self.logger = logging.getLogger(__name__)

    
    def initialize(self):
        pass

    def run(self):
        self.logger.info("FOLLOW LINE")

    def close(self):
        pass