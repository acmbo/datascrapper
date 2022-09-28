"""Test Proxy functionality"""

import os
import sys

#Correct Woking folder
sys.path.append(os.path.abspath(os.path.join('.', 'src')))

from utils.proxy import get_html_via_scrapingapi, get_html_via_tor, get_html_via_webscrapingapi, get_html_via_scrapingapi,local_url
from utils.proxy import scrapingapi_get_request, tor_get_request, webscrapingapi_get_request, local_request
from urllib.request import Request

url_list = ['https://www.dw.com/de//de/mali-einsatz-bringt-deutsche-politiker-immer-stärker-in-wallung/a-59221275',
 'https://www.dw.com/de//de/skandal-oder-kampagne-olaf-scholz-und-die-folgen-einer-razzia/a-59217173',
 'https://www.dw.com/de//de/dw-doku-merkel/a-59192838',
 'https://www.dw.com/de//de/berlin-klimaaktivisten-im-hungerstreik/av-59219778',
 'https://www.dw.com/de//de/algerischer-ex-präsident-abdelaziz-bouteflika-gestorben/a-59220673']


mongo_filter_test = {"url":'/de/wird-russland-belarus-schlucken/a-59181798'}
