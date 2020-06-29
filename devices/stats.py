from datetime import datetime
from utils.db import DB
class Stats:
    def __init__(self, name:str):
        self.name = name
        self.db = DB()
        
    # For Stats
    ## Today stats
    def reset_today_stats(self):
        pass
    
    def increment_today_stats(self):
        pass
    
    def get_today_stats(self) -> str:
        return str(20000)
    
    ## Total stats
    def increment_total_stats(self):
        pass
    
    def get_total_stats(self):
        pass

    ## Last Started
    def set_last_started(self):
        def _get_current_date():
            return datetime.now().strftime("%m-%d-%y %H:%M:%S") 
        
        last_started = self.generate_key_for_db("last_started")
        self.db.write(last_started , _get_current_date())

    
    def get_last_started(self):
        last_started = self.db.read(self.generate_key_for_db("last_started"))
        if last_started is None:
            return "0000-00-00 00:00:00"
        else:
            return last_started


    def generate_key_for_db(self, append_key:str) -> str:
        """
        Returns name+"_"+append_key to store in the db for each device
        eg: motor1_last_run
        """
        return f"{self.name}_{append_key}"

    

