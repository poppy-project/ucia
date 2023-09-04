from abc import ABC, abstractmethod

class BaseController(ABC):
    @abstractmethod
    def process_incoming_commands(self, commands):
        pass

    @abstractmethod
    def get_state(self, id):
        pass

    @abstractmethod
    def get_all_state(self):
        pass

    @abstractmethod
    def reset_robot_state(self):
        pass
    