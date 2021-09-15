import requests
from settings import API_KEY


def get_proxy_data_from_pubproxy():
    """
    Gets a free proxy from pubproxy.com
    Returns:
        (dict): json data from proxy
    """

    url = "http://pubproxy.com/api/proxy?country=DE&type=http"
    response = requests.get(url)   
    
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

    response = requests.request("GET", url_websracpe_api, params=params)

    if response.status_code == 200:
        response.text
        
    else:
        print("GET Response: {s}".format(s=response.status_code))
        return None


if __name__=="__main__":
    
    url="www.dw.com/de"
    html=get_html_via_webscrapingapi(url)

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all("div")



