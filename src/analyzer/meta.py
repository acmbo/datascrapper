"""Analyzer for meta of data"""
import json
import requests
from arc import Analyzer


class Meta_Analyzer(Analyzer):
    """Analyzer to process meta data from scrapper and send it to server

    Args:
        Analyzer (parent): metaclass, which inherits basic db operations to work with redis db.
    """
    
    def __init__(self, dbnumber):
        super().__init__(dbnumber)
        self.data = {}
        self.url_internal = "http://127.0.0.1:5000/meta/scrapper/"
        self.url = "http://stephanscorner.de/meta/scrapper/"
        self.meta_filepath = "scrapper_meta.json"
    
    
    def post_to_api(self, internal=True):
        """post objects data to server api. Internal argument used for determining if you post to a internalt test server or to productive online server

        Args:
            internal (bool, optional): Send data to internal test server or online productive system. Defaults to True, which sends data to internal test server.
        """
        if len(self.data) > 0:
            try:
                post_data = {
                    'name':self.data["Scrapper"],
                    'entries':self.data["Articles"],
                    'date':self.data["StartTime"],
                    'errors':self.data["Errors"],
                }
            except Exception as e:
                print("Encounterd Error: ",e)
                return None
        
        if internal:
            response = requests.post(self.url_internal, json=post_data)
        else:
            response = requests.post(self.url, json=post_data)
        
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
    test.write_to_json()
    test.post_to_api()
    post_data = {
    'name':test.data["Scrapper"],
    'entries':test.data["Articles"],
    'date':test.data["StartTime"],
    'errors':test.data["Errors"],
    }
    response = requests.post("http://127.0.0.1:5000/meta/scrapper/", json=post_data)
    print(response)
    
    response = requests.get("http://127.0.0.1:5000/meta/scrapper/")
    print(response)
    print(response.json())
    

from urllib.parse import urlencode
request_dict = post_data 
data = {
    'Request': json.dumps(request_dict)     # formats the dict to json text
}

r = requests.post("http://127.0.0.1:5000/meta/scrapper/", data=json.dumps(post_data))

req = requests.Request('POST',"http://127.0.0.1:5000/meta/scrapper/",headers={'X-Custom':'Test'},data=json.dumps(post_data))
prepared = req.prepare()

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

pretty_print_POST(prepared)

req.