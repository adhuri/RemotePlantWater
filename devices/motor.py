from devices.device import Device
import time

import logging 
logger = logging.getLogger("water_plants")


class Motor(Device):

    
    def start(self):
        pump_duration = int(self.readConfig("PumpDuration"))
        pump = int(self.readConfig("DefaultPump"))
        logger.info(f"Starting Motor: \"{self.name}\" with {pump} pumps")   
        logger.debug(f"Running for {pump_duration} seconds")
        self.turnONGPIO()
        time.sleep(pump_duration)
             
    def stop(self):
        logger.info(f"Stopping Motor: \"{self.name}\"")   
        self.turnOFFGPIO()
