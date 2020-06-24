import atexit
from devices.motor import Motor
from logger import init_logger

if __name__ == "__main__":
    init_logger()
    m = Motor(name = "Motor Indoor", bcm_pin_number = 2)
    m.start()
    m.stop()

atexit.register(m.cleanUpGPIO)
