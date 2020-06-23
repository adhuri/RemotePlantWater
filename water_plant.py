import logging

from devices.motor import Motor
import atexit
logger = logging.getLogger("water_plants")
logger.setLevel(level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(name)-4s %(levelname)-8s %(message)s')
ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
ch.setFormatter(formatter)

fh = logging.FileHandler('water_plant.log')
fh.setLevel(level=logging.INFO)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)


if __name__ == "__main__":
    m = Motor(name = "Motor Indoor", bcm_pin_number = 2)
    m.start()
    m.stop()

atexit.register(m.cleanUpGPIO)
