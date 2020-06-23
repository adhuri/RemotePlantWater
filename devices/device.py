from abc import ABC

class Device(ABC):
    def __init__(type:str):
        self.type = type
        super().__init__()

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

