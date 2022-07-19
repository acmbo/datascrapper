"""Analyzer for meta of data"""
import json
import requests
from .arc import Analyzer


class Meta_Analyzer(Analyzer):
    """Analyzer to process meta data from scrapper and send it to server

    Args:
        Analyzer (parent): metaclass, which inherits basic db operations to work with redis db.
    """
    
    def __init__(self, dbnumber, data=None):
        super().__init__(dbnumber)
        self.data = {}
        self.url_internal = "http://127.0.0.1:5000/meta/scrapper/"
        self.url = "http://stephanscorner.de/meta/scrapper/"
        self.meta_filepath = "scrapper_meta.json"
        if data:
            self.data = data
    
    
    def post_to_api(self, internal=True):
        """post objects data to server api. Internal argument used for determining if you post to a internalt test server or to productive online server

        Args:
            internal (bool, optional): Send data to internal test server or online productive system. Defaults to True, which sends data to internal test server.
        """
        if len(self.data) > 0:
            try:
                post_data = {
                    'name': (None, self.data["Scrapper"]),
                    'entries':(None, self.data["Articles"]),
                    'date':(None, self.data["StartTime"]),
                    'errors':(None, self.data["Errors"]),
                }
            except Exception as e:
                print("Encounterd Error: ",e)
                return None
        
        if internal:
            response = requests.post(self.url_internal, files=post_data)
        else:
            response = requests.post(self.url, files=post_data)
        
        return response
            
            
    def read_meta_json(self):
        """Reads data from scrapper_meta json which is created by slug.py
        """
        with open(self.meta_filepath, 'r') as f:
            jsonstring = json.load(f)
            
        self.data = json.loads(jsonstring)
        
        
    def write_to_json(self):
        """Writes back changes to scrappermeta json.
        """
        json_string = json.dumps(self.data)
        
        with open(self.meta_filepath, "w") as i :
            json.dump(json_string, i)
        
        
            
if __name__ == "__main__":
    
    test = Meta_Analyzer(1)
    test.read_meta_json()
    r = test.post_to_api()
    print(r)