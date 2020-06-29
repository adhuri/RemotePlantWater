import shelve
import logging 
from threading import Lock
from definitions import ROOT_DIR
logger = logging.getLogger("water_plants")




class DB:
    filename = f"{ROOT_DIR}/utils/shelvedb"
    mutex = Lock()

    def open(self):
        self.d = shelve.open(self.filename)
    
    def close(self):
        self.d.close()

    def write(self, key:str, value: str) -> bool:
        self.mutex.acquire()
        try:
            self.open()
            self.d[key] = value
            logger.debug(f"db [write] - {key}:{value}")
            self.close()
            self.mutex.release()
            return True
        except Exception as e:
            logger.error(f"Unable to write key:{key}, value:{value} due to {e}")
            self.close()
            self.mutex.release()
            return False



    def read(self, key:str) -> str:
        self.mutex.acquire()
        try:
            self.open()
            val = self.d[key]
            logger.debug(f"db [read] - {key}:{val}")
            self.close()
            self.mutex.release()
            return val
        except KeyError:
            logger.error(f"db [read] - No key found :{key}")
            self.close()
            self.mutex.release()
            return None



