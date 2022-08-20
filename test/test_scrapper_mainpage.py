
import pytest
import os
import sys
from pathlib import Path

#Correct Woking folder
sys.path.append(os.path.abspath(os.path.join('..', 'src')))
sys.path.append(os.path.abspath(os.path.join('.', 'src')))

from utils.proxy import choose_proxy_from_proxyrotation
from dw.article_v_02 import extract_article_data
from scrape_dw import scrape_dw_theme_page




def test_completeScrapper() -> None:
    
    choosen_proxy = choose_proxy_from_proxyrotation()
    base = "https://www.dw.com"


    print("scraping with {prox}".format(prox = str(choosen_proxy[0])))
    html = choosen_proxy[0](base+ "/de")
    articles = scrape_dw_theme_page(html)


    proecessed_articles = []

    for art in articles:
        
        choosen_proxy = choose_proxy_from_proxyrotation()
        
        print("scraping with {prox}".format(prox = str(choosen_proxy[0])))
        html = choosen_proxy[0](base+art["url"])

        if html:
            proecessed_articles.append(extract_article_data(art, html))
            
        