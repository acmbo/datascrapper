if __name__ == "__main__":
    
    import sys
    import os
    
    currentpath = os.getcwd()
    sys.path.append(os.path.abspath(os.path.join(currentpath, os.pardir)))
    

from random import randint
from bs4 import BeautifulSoup as bs

import requests
import time 
import json

from utils.loggers import createStandardLogger  
from utils.proxy import choose_proxy_from_proxyrotation
from db.redis_dw import get_db, get_dw_article_by_url, add_article_hashset

#SLEEPTIME = randint(3,10)
SLEEPTIME = 1

logger = createStandardLogger(__name__)


def get_ready_soup_html(url:str, proxy=None):
    """_summary_

    Args:
        url (str):str of url

    Returns:
        soup: soup of beatiful soup, ready html for further analysis
    """
    if proxy:
        try:
            soup = proxy(url)
            
            if soup is None:
                logger.error("Error in Slug: Empty html.  {url}\n ".format(
                                                                url=str(url)))
                return None
            else:                            
                return soup
        except Exception as e:
            logger.error("Error in Slug: {url} = \n {e} ".format(e=e,
                                                                url=str(url)))
            return None
    
    try:
        req =  requests.get(url)
        soup = bs(req.text)
        return soup
    
    except Exception as e:
        print("ERROR: ", e)
        return None


def get_all_hrefs_from_page(soup, add_root_page: str = ""):
    """Returns a list of urls ready for use

    Args:
        soup (bs4.soup): soup of html

    Returns:
        list: list of urls
    """
    # get all links
    hrefs = [link.get('href') for link in soup.find_all('a') ]
    
    # remove nones
    hrefs = [link for link in hrefs if link != None]
    
    # Removes external links
    hrefs = [href for href in hrefs if "https://www.spiegel.de/" in href]
    #adds a root page to all hrefs
    if add_root_page != "":
        hrefs = [add_root_page + href for href in hrefs]
        
    return hrefs


def check_html_for_site_type(soup, s_type = "article"):
    """Checks if html is a article by defintion of reuters page.
    Known types:
    -article
    -article:section

    Args:
        soup (bs4.soup): soup of html

    Returns:
        bool: true if article
    """
    for findings in soup.head.find_all("meta", {"property":"og:type"}):
        if "content" in findings.attrs.keys():
            if s_type == findings["content"]:
                return True
    return False


def get_empty_article_data_dict():
    
    article_data = {
        "r_site_type":"",
        "url":"",
        "title":"",
        "urls":""
    }
    return article_data


def get_content(soup, tag: str, props: dict):
    """get content from a bs4 query. 
    Query example: soup.head.find("meta", {"property":"og:type1"})

    Args:
        soup (bs4.soup): soup of html
        tag (str): html tag
        porps (dict): propetry to search for

    Returns:
        str: content as string
    """
    if soup.head.find(tag, props):
        
        if "content" in soup.head.find(tag, props).attrs:
            return soup.head.find(tag, props)["content"]
        else:
            return soup.head.find(tag, props)
    return ""



def get_settings_script_content(soup):
    tag = "script"
    jsoncontent = soup.find(tag,{"type":"application/settings+json"})
    if jsoncontent:
        for child in list(jsoncontent.children):
            try:
                j = json.loads(str(child))
                paywall_active = j["paywall"]["attributes"]["is_active"]
                theme = j["page"]["attributes"]['channel_slug']
                subtheme = j["page"]["attributes"]['subchannel_slug']
                return (paywall_active, theme, subtheme)
            
            except Exception as e:
                print("No settings+json found")
                logger.error(f"Spiegel error in scraping: {e}")
    return None
    
    
def get_page_data(soup):
    """Extracts data from website

    Args:
        soup (bs4.soup): soup of html

    Returns:
        dict: article data as ditcionary
    """
    article_data = get_empty_article_data_dict()

    # Check for page type
    if check_html_for_site_type(soup,s_type="article"):
        settingsinfo = get_settings_script_content(soup)

        if settingsinfo == None: raise Exception("No settings content found")

        paywall_active, theme, subtheme = settingsinfo

        article_data["paywall_active"] = paywall_active
        article_data["theme"] = theme
        article_data["subtheme"] = subtheme
        article_data["r_site_type"] = "article"
        article_data["sitetitle"] = soup.title
        article_data["description"] = get_content(soup, "meta",  {"name":"description"})
        article_data["published_time"] = get_content(soup, "meta",  {"name":"date"})
        article_data["modified_time"] = get_content(soup, "meta",  {"name":"last-modified"})
        article_data["author"] = get_content(soup, "meta",  {"name":"author"})
        article_data["locale"] = get_content(soup, "meta",  {"name":"locale"})
        article_data["title"] = get_content(soup, "meta",  {"property":"og:title"})
        article_data["url"] = get_content(soup, "meta",  {"property":"og:url"})
        article_data['Schlagwörter']  = get_content(soup, "meta",  {"name":"news_keywords"}).split(", ")   #should be a list
    
    elif check_html_for_site_type(soup,s_type="website"):
        article_data["urls"] = get_all_hrefs_from_page(soup, add_root_page="")
        article_data["r_site_type"] = "website"
    
    return article_data




def scrape_spiegel(db):
    """scraping function to scrape spiegel data on website. Adds all article data to redis db instance

    Args:
        db (db instance): redis database

    """
    already_visited_sites = []
    known_article_sections = ["https://www.spiegel.de/"]
    found_articles = []
    data = []
    blacklist = []

    found_articles.extend(known_article_sections)
    root_page = "https://www.spiegel.de" # Remove last backslash

    # read blacklist and prepare links
    with open('blacklist.txt') as f:
        blacklist = f.readlines()
    blacklist = [link.replace("\n","") for link in blacklist]

    
    i = 0
    article_idx = len(found_articles)
    
    while i <= article_idx:
    #while i <= 30:
        
        # Get url
        url = found_articles[i]
        
        print("sleeping..")
        
        time.sleep(SLEEPTIME)
        
        print(url)
        
        # url in db
        redsidbdata = get_dw_article_by_url(db, url, hset=True)
        if redsidbdata:
            continue
        
        # check if url already in current cycle
        if url not in already_visited_sites:
            # get ready soup for analysis. If soup == None, because url is unavailabe, skip site.
            proxy = choose_proxy_from_proxyrotation(local_request=0.5,
                                        get_html_via_tor=0.5,
                                        get_html_via_webscrapingapi=0.0,
                                        get_html_via_scrapingapi=0.0)    # load a proxy for consistency of code

            soup = get_ready_soup_html(url, proxy=proxy)
            
            if soup:
                hrefs = get_all_hrefs_from_page(soup, add_root_page="")

                #Filter hrefs
                def filterfunc(link):
                    validHref = link
                    for blacklistLink in blacklist:
                        if blacklistLink in validHref:
                            return None
                    return validHref
                
                hrefs = [href for href in hrefs if filterfunc(href) != None]
                
                #Track site
                already_visited_sites.append(url)
                try:
                    article_data = get_page_data(soup)
                    
                    # Check page type
                    if article_data["r_site_type"] == "website":
                        
                        #Add urls to found articles, so you expand the data of website
                        for _url in article_data["urls"]:
                            
                            if _url not in found_articles:
                                found_articles.append(_url)
                                article_idx +=1
                                
                            if _url not in known_article_sections:
                                known_article_sections.append(_url)
                                
                    elif article_data["r_site_type"] == "article":

                        data.append(article_data)
                        
                        
                except Exception as e:
                    logger.error(f"Spiegel error in scraping: {e}")
                    continue        
        i+=1
        
        for entry in data:
            add_article_hashset(db, entry)





if __name__ == "__main__":
    
    import sys
    import os
    
    currentpath = os.getcwd()
    sys.path.append(os.path.abspath(os.path.join(currentpath, os.pardir)))
    
    already_visited_sites = []
    known_article_sections = ["https://www.spiegel.de/"]
    found_articles = []
    data = []
    blacklist = []

    found_articles.extend(known_article_sections)
    root_page = "https://www.spiegel.de" # Remove last backslash

    # read blacklist and prepare links
    with open('blacklist.txt') as f:
        blacklist = f.readlines()
    blacklist = [link.replace("\n","") for link in blacklist]

    
    i = 0
    article_idx = len(found_articles)
    
    while i <= article_idx:
    #while i <= 30:
        
        # Get url
        url = found_articles[i]
        
        print("sleeping..")
        
        time.sleep(SLEEPTIME)
        
        print(url)
        
        # url in db
        redsidbdata = get_dw_article_by_url(db, url, hset=True)
        if redsidbdata:
            continue
        
        # check if url already in current cycle
        if url not in already_visited_sites:
            # get ready soup for analysis. If soup == None, because url is unavailabe, skip site.
            proxy = choose_proxy_from_proxyrotation(local_request=0.5,
                                        get_html_via_tor=0.5,
                                        get_html_via_webscrapingapi=0.0,
                                        get_html_via_scrapingapi=0.0)    # load a proxy for consistency of code

            soup = get_ready_soup_html(url, proxy=proxy)
            
            if soup:
                hrefs = get_all_hrefs_from_page(soup, add_root_page="")

                #Filter hrefs
                def filterfunc(link):
                    validHref = link
                    for blacklistLink in blacklist:
                        if blacklistLink in validHref:
                            return None
                    return validHref
                
                hrefs = [href for href in hrefs if filterfunc(href) != None]
                
                #Track site
                already_visited_sites.append(url)
                try:
                    article_data = get_page_data(soup)
                    
                    # Check page type
                    if article_data["r_site_type"] == "website":
                        
                        #Add urls to found articles, so you expand the data of website
                        for _url in article_data["urls"]:
                            
                            if _url not in found_articles:
                                found_articles.append(_url)
                                article_idx +=1
                                
                            if _url not in known_article_sections:
                                known_article_sections.append(_url)
                                
                    elif article_data["r_site_type"] == "article":

                        data.append(article_data)
                        
                        
                except Exception as e:
                    logger.error(f"Spiegel error in scraping: {e}")
                    continue        
        i+=1
        
        for entry in data:
            add_article_hashset(db, entry)




