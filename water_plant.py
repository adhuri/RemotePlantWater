from devices.motor import Motor
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-4s %(levelname)-8s %(message)s',
                    datefmt='%m-%d-%Y %H:%M:%S')

if __name__ == "__main__":
    m = Motor(name = "Motor Indoor")
    m.start()
    m.stop()
