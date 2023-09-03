import logging
from tasks.base import Task
from controller.base import BaseController

class FollowLine(Task):
    def __init__(self, controller: BaseController):
        self.controller = controller
        self.logger = logging.getLogger(__name__)

    
    def initialize(self):
        pass

    def run(self):
        self.logger.info("FOLLOW LINE")

    def close(self):
        pass