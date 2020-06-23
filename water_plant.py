from devices.motor import Motor
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

if __name__ == "__main__":
    m = Motor(name = "Motor Indoor")
    m.start()
    m.stop()
