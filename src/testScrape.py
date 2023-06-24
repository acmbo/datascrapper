import time
import random
import json
import slug

from utils.proxy import choose_proxy_from_proxyrotation
from utils.time import time_is_passed_by_actualTime, \
    select_random_time_of_a_day, get_actual_datetime, check_change_of_day_in_datetimevalues
from utils.loggers import createStandardLogger    
from utils.settings import proxy_probabiltys

from scrape_dw import scrape_dw_theme_page
from dw.utils_article import remove_double_entrys_in_article
from dw.article_v_02 import extract_article_data
from db.redis_dw import get_db, add_article_hashset, check_url_exist, REDISDB



if __name__ == "__main__":
    
    meta = {}

    
    meta["StartTime"] = get_actual_datetime().isoformat()
    meta["Articles"] = 0
    meta["Scrapper"] = "Raspberry Pi 2+"
    meta["Errors"] = 0
    
    url_source = "https://www.dw.com"     # Needed fpr building hrefs-urls

    extracted_articles = slug.get_dw_front_pages_data()

    #random_int = 0  #commented out from former version of the script
    
    proxy = choose_proxy_from_proxyrotation(local_request=1.0,
                                            get_html_via_tor=0.0,
                                            get_html_via_webscrapingapi=0.0,
                                            get_html_via_scrapingapi=0.0)    # load a proxy for consistency of code
    backed_arts = []


    for idx, art in enumerate(extracted_articles):
        
        proxy = choose_proxy_from_proxyrotation(local_request=1.0,
                                                get_html_via_tor=0.0,
                                                get_html_via_webscrapingapi=0.0,
                                                get_html_via_scrapingapi=0.0)    # load a proxy for consistency of code
    
        

            
        exartlen = len(extracted_articles)
        

        status , extracted_articles = slug.execute_get_request_article(proxy_func = proxy[0],
                                    _url_source=url_source,
                                    article=art,
                                    _db = None,
                                    extracted_articles=extracted_articles,
                                    idx=idx)
        