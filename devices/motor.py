from devices.device import Device
import logging 
import time


class Motor(Device):

    
    def start(self):
        pump_duration = int(self.readConfig("PumpDuration"))
        pump = int(self.readConfig("DefaultPump"))
        logging.info(f"Starting Motor: \"{self.name}\" with {pump} pumps")   
        logging.debug(f"Running for {pump_duration} seconds")
        time.sleep(pump_duration)
             
    def stop(self):
        logging.info(f"Stopping Motor: \"{self.name}\"")        