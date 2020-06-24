import configparser
import logging
import mock
from abc import ABC, abstractmethod


logger = logging.getLogger("water_plants")


try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    logger.error("Can't import GPIO, Non Raspberry PI device. Mocking for development")
    GPIO = mock.Mock
    GPIO.LOW, GPIO.HIGH, GPIO.BCM, GPIO.OUT = None, None, None, None
    GPIO.output = mock.Mock
    GPIO.cleanup = mock.Mock
    GPIO.setup = mock.Mock
    GPIO.setmode = mock.Mock

class Device(ABC):
    
    def __init__(self, name:str, bcm_pin_number:int):
        self.name = name
        self.bcm_pin_number = bcm_pin_number
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.initGPIO()
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

    def initGPIO(self):
        logging.debug(f"Init GPIO BCM pin {self.bcm_pin_number}")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bcm_pin_number, GPIO.OUT)
        

    def turnONGPIO(self):
        logger.debug(f"ON GPIO BCM pin {self.bcm_pin_number}")
        GPIO.output(2, GPIO.LOW)

    def turnOFFGPIO(self):
        logger.debug(f"OFF GPIO BCM pin {self.bcm_pin_number}")
        GPIO.output(2, GPIO.HIGH)
    
    def cleanUpGPIO(self):
        logger.debug(f"Cleanup GPIO")
        GPIO.cleanup()





