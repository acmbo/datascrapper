import requests
import time
import random
from settings import API_KEY
from torpy import TorClient
from torpy.utils import recv_all
from torpy.http import requests as tor_request
from torpy.http.adapter import TorHttpAdapter



def get_html_via_tor(url: str):
    
    try:
        with TorClient() as tor:
            with tor.get_guard() as guard:
                adapter = TorHttpAdapter(guard,3)
                with requests.Session() as sess:
                    #sess.headers.update({'User-Agent':'Mozilla/5.0'})            
                    sess.mount('http://', adapter)
                    sess.mount('https://', adapter)
                    
                    
                    resp = sess.get(url,timeout=15)
                    
                    if resp.status_code == 200:
                        return resp.text
                    
                    else:
                        return None
    except:
        return None
                

def get_multiple_html_via_tor(urls: list):
    
    return_list = []
    
    try:
        
        with TorClient() as tor:
            
            with tor.get_guard() as guard:
                adapter = TorHttpAdapter(guard,3)
                
                with requests.Session() as sess:
                    #sess.headers.update({'User-Agent':'Mozilla/5.0'})            
                    sess.mount('http://', adapter)
                    sess.mount('https://', adapter)
                    
                    for url in urls:
                        
                        resp = sess.get(url,timeout=15)
                        
                        if resp.status_code == 200:
                            return_list.append(resp.text)
                        
                        else:
                            return_list.append(None)
                            
                        time.sleep(random.randint(15,30))
        
        return return_list
    
    except:
        return None
            

def get_proxy_data_from_pubproxy():
    """
    Gets a free proxy from pubproxy.com
    Returns:
        (dict): json data from proxy
    """

    url = "http://pubproxy.com/api/proxy?country=DE&type=http"
    
    try:
        response = requests.get(url)   
        
    except:
        return None
    
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_html_via_webscrapingapi(url: str, **kwargs):
    """get html text as str from an website via webscraping api
    from https://api.webscrapingapi.com

    Args:
        url (str): target url
        ** kwargs: parameters for webscraper, so documentation webscrapingapi

    Returns:
        str: html as str or None if response != 200
    """
    
    
    url_websracpe_api = "https://api.webscrapingapi.com/v1"

    params = {
    "api_key":API_KEY,
    "url":url,
    "country":"de"
    }

    try:
        response = requests.request("GET", url_websracpe_api, params=params)

        if response.status_code == 200:
            return response.text
            
        else:
            print("GET Response: {s}".format(s=response.status_code))
            return None
        
    except:
        return None


if __name__=="__main__":
    
    url = "https://www.dw.com/de"
    html = get_html_via_webscrapingapi(url)

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all("div")



