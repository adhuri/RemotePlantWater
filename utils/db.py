import shelve
import logging 
logger = logging.getLogger("water_plants")

class DB:
    filename = "./utils/shelvedb"

    def open(self):
        self.d = shelve.open(self.filename)
    
    def close(self):
        self.d.close()

    def write(self, key:str, value: str) -> bool:
        try:
            self.open()
            self.d[key] = value
            self.close()
            return True
        except Exception as e:
            logger.error(f"Unable to write key:{key}, value:{value} due to {e}")
            return False



    def read(self, key:str) -> str:
        try:
            self.open()
            return self.d[key]
        except KeyError:
            logger.error(f"No key found :{key}")
            return None



