from abc import ABC, abstractmethod

class Task(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def close(self):
        pass