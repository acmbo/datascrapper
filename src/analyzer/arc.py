"""utility class and functions for data analysis"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))

import numpy as np
from db.redis_dw import get_db,  get_all_dw_article,  get_dw_article_by_url


def get_redis_data(db):
    """Generator for returning data from redis db"""
    keys = np.array(get_all_dw_article(db))
    for key in keys:
        #print("KEY: ", key)
        yield get_dw_article_by_url(db, key, hset=True)


class Analyzer:
    """Analyzer Meta Class
    """
    def __init__(self, dbnumber):
        self.used_db = dbnumber
        pass
    
    def connect_to_db(self):
        db = get_db()
        return db
    
    def get_data(self):
        redis_data =   [] # np.array([])
        
        with self.connect_to_db() as db:
            for data in get_redis_data(db):
                try: 
                    key=data["url"]
                    val=data["Datum"]
                except:
                    #print("Error on ", data)
                    key = None
                    val = None
                redis_data.append((key, val))
                
        return np.array(redis_data)
    
if __name__ =="__main__":
    an = Analyzer(1)
    rd = an.get_data()
    #print(rd)
    from datetime import datetime
    new_arr = []
    for d in rd:
        if isinstance(d[1], str) and d[1] != "":
            print("KEY: ", d[1])
            datetime_object = datetime.strptime(d[1], '%d.%m.%Y')
            print(datetime_object)
    
    
    