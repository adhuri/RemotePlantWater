from abc import ABC, abstractmethod
import configparser

class Device(ABC):
    
    def __init__(self, name:str):
        self.name = name
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        super().__init__()

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    def readConfig(self, config_name:str) -> str :
        if self.name in self.config:
            device_config = self.config[self.name]
            config_value = device_config.get(config_name)
            if config_value is not None:
                return config_value 
            else:
                raise KeyError(f"key: {config_name} not found under {self.name} in config.ini")
        else:
            raise Exception(f"message: Device config not found : {self.name}")




