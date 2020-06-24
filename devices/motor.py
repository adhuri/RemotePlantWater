from devices.device import Device
import time
from typing import Dict
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

    def run(self):       
        cycles = self.no_of_cycles()
        logger.info(f"Running the pump for cycles : {cycles}")
        for cycle in range(1,cycles+1):
            logger.info(f"Cycle No: {cycle}")
            self.start()
            self.stop()
            logger.debug(f"Waiting for duration in seconds: {self.duration_between_cycles()}")
            time.sleep(self.duration_between_cycles())

    def get_schedule(self) -> [str,str,str]:
        return self.readConfig("ScheduledDateTime").split(":")

    def no_of_cycles(self) -> int:
        return int(self.readConfig("Cycles"))

    def duration_between_cycles(self) -> int:
        return int(self.readConfig("DurationBetweenCycles"))