import logging

from controller.base import BaseController
from tasks.base import Task

class ObjectCollector(Task):
    def __init__(self, controller: BaseController):
        self.controller = controller
        self.logger = logging.getLogger(__name__)

    def initialize(self):
        pass

    def run(self):
        self.logger.info("OBJECT COLLECTOR")

    def close(self):
        pass