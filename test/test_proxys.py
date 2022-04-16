"""Test Proxy functionality"""

import os
import sys

#Correct Woking folder
sys.path.append(os.path.abspath(os.path.join('.', 'src')))

from utils.proxy import get_html_via_scrapingapi, get_html_via_tor, get_html_via_webscrapingapi, get_html_via_scrapingapi,local_url
from utils.proxy import scrapingapi_get_request, tor_get_request, webscrapingapi_get_request, local_request


testapi='https://api.ipify.org' #Returns current api adress

def test_tor():
    test=tor_get_request(testapi)
    assert test.status_code == 200 

def test_local():
    test = local_url(testapi)    
    assert test.status == 200 

def test_websc():
    test=webscrapingapi_get_request(testapi)
    assert test.status == 200 

def test_scrap():
    test=scrapingapi_get_request(testapi)
    assert test.status == 200 


def test_proxys_output():
    test = local_request(testapi) 
    print(test.text)
    
    test2=get_html_via_scrapingapi(testapi)
    print(test2)
    
    test3=tor_get_request(testapi)
    print(test3.text)
    
    test4=get_html_via_webscrapingapi(testapi)
    print(test4)
    
    assert (test.text == test2 == test3.text == test4)
    
    
    
def test_dw_reqeust_All_proxys(): 
    url = "https://www.dw.com/de"
    #html = get_html_via_webscrapingapi(url)
    html_scrapingapi = get_html_via_scrapingapi(url)
    
    if html_scrapingapi != None:
        print("scrapingapi sucess")
    else:
        print("scrapingapiNo Return")

    html_tor = get_html_via_tor(url)

    if html_tor != None:
        print("tor sucess")
    else:
        print("tor No Return")
        
    html_webscrapi = get_html_via_webscrapingapi(url)
    
    if html_webscrapi != None:
        print("webscrapingapi sucess")
    else:
        print("webscrapingapi No Return")
    
    assert ((html_scrapingapi != None) and (html_tor != None) and (html_webscrapi != None))
    
