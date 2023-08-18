from abc import ABC, abstractmethod

class BaseRobot(ABC):
    @abstractmethod
    def fetch_current_state(self):
        pass

    @abstractmethod
    def process_incoming_commands(self, commands):
        pass

    @abstractmethod
    def reset_robot_state(self):
        pass
    