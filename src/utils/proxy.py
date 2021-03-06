import requests
import time
import random
from utils.settings import API_KEY, API_KEY_SCRAPPERYPI
from torpy import TorClient
from torpy.utils import recv_all
from torpy.http import requests as tor_request
from torpy.http.adapter import TorHttpAdapter
from urllib.request import urlopen
from urllib.parse import urlencode



def choose_proxy_from_proxyrotation(**kwargs):
    """function for rotating proxys, through using a random variable between 0 and 1
        the proxys have a probablity as float between 0 and 1 and if the random variable
        falls between the probabiltys of the respectiv functions, the function is returned.
        
        For random choosing starts with 0 till the next probabilty and later on will be added.

        With kwargs the proxy_dict the probiltys can be changed
    Returns:
        (function, int/str): returns the function and the amount of urls, which can be accessed
    """
    
    from collections import namedtuple
    
    Proxy = namedtuple('Proxy', 'function amount_of_usable_urls probability')
    
    #dictionary with proxy functions, amount of processed urls and probablity
    proxy_dict = {
        "local_request": Proxy(local_request, 1, 0.1),
        "get_html_via_tor" : Proxy(get_html_via_tor, 1, 0.1),
        "get_multiple_html_via_tor": Proxy(get_multiple_html_via_tor,'multi', 0.0),
        "get_html_via_webscrapingapi": Proxy(get_html_via_webscrapingapi, 1, 0.4),
        "get_html_via_scrapingapi": Proxy(get_html_via_scrapingapi, 1, 0.4)
    }
    
    #Update probabilitys if passed through kwargs
    proxy_keys = proxy_dict.keys()
    for key, value in kwargs.items():
        if key in proxy_keys and type(value)== float:
            proxy_dict[key] = proxy_dict[key]._replace(probability = value)
    
    
    random_float = random.random()  # Random Number between 0 and 1
    
    
    #print(random_float)
    probabilty = 0
    
    # Choosing one of the functions with a random variable and by using the Probabilty of the proxys
    for key in proxy_dict.keys():
        
        #print("For {s} with probality between {s2} and {s3}".format(s=key, s2=probabilty ,s3=probabilty + proxy_dict[key].probability))
        
        if probabilty <= random_float <  probabilty + proxy_dict[key].probability:
            choosen_proxy = proxy_dict[key].function
            amount_of_urls = proxy_dict[key].amount_of_usable_urls
            #print("now!")
        probabilty += proxy_dict[key].probability
    
    return choosen_proxy, amount_of_urls


def local_request(url:str):
    
    try:
        page = urlopen(url)

        html_bytes = page.read()
        html = html_bytes.decode("utf_8")
        return html
    
    except:
        return None


def get_html_via_tor(url: str):
    """Reqeust via Tor to get html from url website

    Args:
        url (str): target url as string

    Returns:
        (str): html as string or None if reqeust couldnt processed
    """
    
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
    """Request  Website via Tor for multiple urls, which are stored in a list

    Args:
        urls (list): list of urls, saved as strings

    Returns:
        (list): list of extracted html as string or None, if request couldnt processed
    """
    
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




def get_html_via_scrapingapi(url: str, **kwargs):
    """get html text as str from an website via scraping api
    from https://scrapingapi.com

    Args:
        url (str): target url
        ** kwargs: parameters for webscraper, so documentation webscrapingapi

    Returns:
        str: html as str or None if response != 200
    """
    
    
    url_websracpe_api = 'http://api.scraperapi.com/'

    params = {
    "api_key":API_KEY_SCRAPPERYPI,
    "url":url,
    #"country":"de"
    }

    try:
        response = requests.get(url_websracpe_api, 
                        params=urlencode(params))

        if response.status_code == 200:
            return response.text
            
        else:
            print("GET Response: {s}".format(s=response.status_code))
            return None
        
    except:
        return None



if __name__=="__main__":
    
    url = "https://www.dw.com/de"
    #html = get_html_via_webscrapingapi(url)
    html = get_html_via_scrapingapi(url)

    from bs4 import BeautifulSoup

    if html != None:
        soup = BeautifulSoup(html, "html.parser")
        divs = soup.find_all("div")
        print("sucess")
    else:
        print("No Return")



