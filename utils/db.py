import sqlite3
import logging 
from threading import Lock
from definitions import ROOT_DIR
from datetime import datetime
logger = logging.getLogger("water_plants")


class TimestampDB:
    filename = f"{ROOT_DIR}/utils/sqllite.db"
    mutex = Lock()
    def __init__(self, device_name:str):
        try:
            self.device_name = device_name
            conn = sqlite3.connect(self.filename)
            conn.execute('''CREATE TABLE IF NOT EXISTS device_timestamp(
                device_name text,
                device_start timestamp
                )''')
            logger.info("[db] Table:device_timestamp created")
            conn.close()
        except Exception as e:
            logger.error("[db] Couldn't create table")

    def insert_start_timestamp(self) -> bool:
        def _get_current_date():
                return datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        current_date_time = _get_current_date()
        try:
            conn = sqlite3.connect(self.filename)
            c = conn.cursor()
            c.execute('INSERT INTO device_timestamp VALUES (?,?)',(self.device_name, current_date_time))
            conn.commit()
            logger.info(f"[db] Inserted {current_date_time} for {self.device_name}")
            conn.close()
            return True
        except Exception as e:
            logger.error(f"[db] Couldn't insert timestamp {current_date_time} for {self.device_name}")
            return False



    def get_last_timestamp(self) -> str:
        try:
            conn = sqlite3.connect(self.filename)
            c = conn.cursor()
            c.execute('SELECT * FROM device_timestamp WHERE device_name=? ORDER BY device_start DESC LIMIT 1', [self.device_name])
            last_timestamp = c.fetchone()[1]
            logger.info(f"[db] Retrieved device_start timestamp:{last_timestamp} for {self.device_name}")
            conn.close()
            return last_timestamp
        except Exception as e:
            logger.error(f"[db] Couldn't get last timestamp for {self.device_name}")
            return "0000-00-00: 00:00:00"

    
    def get_total_count(self) -> int:
        try:
            conn = sqlite3.connect(self.filename)
            c = conn.cursor()
            c.execute('SELECT * FROM device_timestamp WHERE device_name=?', [self.device_name])
            total_count = len(c.fetchall())
            logger.info(f"[db] Retrieved count:{total_count} for {self.device_name}")
            conn.close()
            return total_count
        except Exception as e:
            logger.error(f"[db] Couldn't get total count for {self.device_name}")
            return -1

    def get_today_count(self) -> int:
        try:
            conn = sqlite3.connect(self.filename)
            c = conn.cursor()
            c.execute('SELECT * FROM device_timestamp WHERE device_name=? AND device_start >= date("now","start of day")', [self.device_name])
            today_count = len(c.fetchall())
            logger.info(f"[db] Retrieved count:{today_count} for {self.device_name}")
            conn.close()
            return today_count
        except Exception as e:
            logger.error(f"[db] Couldn't get today count for {self.device_name}")
            return -1

    
