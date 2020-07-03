from devices.device import Device
import time
from typing import Dict
import logging 
logger = logging.getLogger("water_plants")


class Motor(Device):

    
    def start(self, duration = None):
        if duration:
            pump_duration = duration
        else:
            pump_duration = self.default_pump_duration()
        pump = int(self.readConfig("DefaultPump"))
        logger.info(f"Starting Motor: \"{self.name}\" with {pump} pumps")   
        logger.info(f"Running for {pump_duration} seconds")
        self.turnONGPIO()
        time.sleep(pump_duration)
        self.db.insert_start_timestamp()

             
    def stop(self):
        logger.info(f"Stopping Motor: \"{self.name}\"")   
        self.turnOFFGPIO()

    def run(self, on_demand_cycles = None):
        if on_demand_cycles:       
            cycles = on_demand_cycles 
            logger.info("On demand water requested.")
        else:
            cycles = self.no_of_cycles()
        logger.info(f"Running the pump for cycles : {cycles}")
        for cycle in range(1,cycles+1):
            logger.info(f"Cycle No: {cycle}")
            self.start()
            self.stop()
            logger.debug(f"Waiting for duration in seconds: {self.duration_between_cycles()}")
            time.sleep(self.duration_between_cycles())

    def get_schedule(self) -> [str,str,str]:
        schedule_date_times = []
        for time in self.readConfig("ScheduledDateTime").split(","):
            schedule_date_times.append(time.split(":"))
        return schedule_date_times

    def no_of_cycles(self) -> int:
        return int(self.readConfig("Cycles"))

    def duration_between_cycles(self) -> int:
        return int(self.readConfig("DurationBetweenCycles"))

    def default_pump_duration(self) -> int:
        return int(self.readConfig("PumpDuration"))