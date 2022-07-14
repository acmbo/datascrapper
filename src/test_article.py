from dw.article import extract_article_data

from utils.proxy import get_html_via_scrapingapi, get_html_via_tor, get_html_via_webscrapingapi, get_html_via_scrapingapi,local_url
from utils.proxy import scrapingapi_get_request, tor_get_request, webscrapingapi_get_request, local_request

from dw.mainpage import get_empty_article_meta_data


def preprocess_meta_data(article: dict):
    """preprocesses the data inside article dictionary for later
       readybilty within python. Changes not python standard datatypes
       to string (like bs4.element.tag datatyoe)

    Args:
        article (dict): article dictionary containing article data

    Returns:
        article (dict): preprocessed dictionary
        
    """
    
    for key, val in article.items():
        if type(val) == bool:
            continue
        elif type(val) == str:
            continue
        elif type(val) == list:
            article[key] = [str(entry) for entry in val]
        elif type(val) == dict:
            continue
        else:
            article[key] = str(val)
            
    return article


url = "https://www.dw.com/de/bild-des-tages-blusen-f%C3%BCr-den-frieden/g-45442037"
url = "https://www.dw.com/de/die-operngala-bonn-2022-gro%C3%9Fe-arien-starke-stimmen/av-61877484"
test = local_request(url) 

article = get_empty_article_meta_data()
article = extract_article_data(article, test)

x = preprocess_meta_data(article)












import time
import random
from utils.proxy import choose_proxy_from_proxyrotation
from utils.time import time_is_passed_by_actualTime, \
    select_random_time_of_a_day, get_actual_datetime, check_change_of_day_in_datetimevalues
from utils.loggers import createStandardLogger    
from utils.settings import proxy_probabiltys
from scrape_dw import scrape_dw_theme_page
from dw.utils_article import remove_double_entrys_in_article
from dw.article import extract_article_data
#from db.mongo import get_db, add_article, check_url_exist
from db.redis_dw import get_db, add_article_hashset, check_url_exist



logger = createStandardLogger(__name__)


local_request = proxy_probabiltys["local_request"]
get_html_via_tor = proxy_probabiltys["get_html_via_tor"]
get_html_via_webscrapingapi = proxy_probabiltys["get_html_via_webscrapingapi"]
get_html_via_scrapingapi = proxy_probabiltys["get_html_via_scrapingapi"]


def preprocess_meta_data(article: dict):
    """preprocesses the data inside article dictionary for later
       readybilty within python. Changes not python standard datatypes
       to string (like bs4.element.tag datatyoe)

    Args:
        article (dict): article dictionary containing article data

    Returns:
        article (dict): preprocessed dictionary
        
    """
    
    for key, val in article.items():
        if type(val) == bool:
            continue
        elif type(val) == str:
            continue
        elif type(val) == list:
            article[key] = [str(entry) for entry in val]
        elif type(val) == dict:
            continue
        else:
            article[key] = str(val)
            
    return article


def extract_articles_from_urlist_of_dw_theme_pages(urls: list):
    """extracts article urls an main data from dw.com theme(front) pages

    Args:
        urls (list): list of urls as string

    Returns:
        extracted articles (list): extracted list of dw pages
        
    """
    
    extracted_articles = []
    
    for url in urls:
        #get random proxy
        
        run=True
        print(url)
        
        logger.info("current url: {_url}".format(_url=url))
        
        while run:
            
            sleeptime = random.randint(5,10)
            
            logger.info("sleeping {num} secs...".format(num=sleeptime))
            
            time.sleep(sleeptime)
            
            choosen_proxy = choose_proxy_from_proxyrotation(local_request=local_request,
                                                            get_html_via_tor=get_html_via_tor,
                                                            get_html_via_webscrapingapi=get_html_via_webscrapingapi,
                                                            get_html_via_scrapingapi=get_html_via_scrapingapi)
            
            logger.info("scraping with {prox}".format(prox = str(choosen_proxy[0])))
            
            html = choosen_proxy[0](url)  
            
            if html:  
                extracted_articles.extend(scrape_dw_theme_page(html))
                run=False
            else:
                logger.error("Couldnt extract page")
                
        logger.info("------------------------------------------------------")    
    
    return extracted_articles



def get_dw_front_pages_data():
    """Function for extraacting front page data of dw. Returns a list of articles as dictionarys

    Returns:
        [type]: [description]
    """
    
    urls = ["https://www.dw.com/de/",
            "https://www.dw.com/de/themen/wissen-umwelt/s-12296",
            "https://www.dw.com/de/themen/kultur/s-1534",
            "https://www.dw.com/de/themen/sport/s-12284",
            "https://www.dw.com/de/themen/welt/s-100029",
            "https://www.dw.com/de/wirtschaft/s-1503"]



    extracted_articles = extract_articles_from_urlist_of_dw_theme_pages(urls)
            
            
    #Remove double entrys
    extracted_articles, double_hrefs = remove_double_entrys_in_article(extracted_articles)

    logger.info("Finished Extraction")

    return extracted_articles


def execute_get_request_article(proxy_func, _url_source, article, _db, extracted_articles, idx):
    """Execution of request for article

    Args:
        proxy_func (func): choosen proxyfunction
        _url_source (str): source url of dw website
        article (dict): article dictionary
        _db (redis.db): instance redis db
        extracted_articles(list): current articles list
        idx(int): current index
    """
    try:
        html = proxy_func(_url_source + article['url'])
        
        if html is None:
            logger.error("Error in Slug: Empty html.  {url}\n ".format(
                                                            url=str(_url_source + article['url'])))
            return 1, extracted_articles
            
        else: 
            extracted_articles[idx] = preprocess_meta_data(extract_article_data(article, html))
            #add_article_hashset(_db, extracted_articles[idx])
            logger.info(" -- Sucessfull scraped {url} -- ".format(url=_url_source + article['url']))
            return 0, extracted_articles
            
    except Exception as e:
        logger.error("Error in Slug: {url} = \n {e} ".format(e=e,
                                                            url=str(_url_source + article['url'])))
        return 1, extracted_articles
        



logger.info("Start new Crawl")
url_source = "https://www.dw.com/"  
x=get_empty_article_meta_data()
x["url"]="/de/bild-des-tages-blusen-f%C3%BCr-den-frieden/g-45442037"
y=get_empty_article_meta_data()
y["url"] = "/de/das-gefährliche-leben-der-zugvögel/a-61661785"
extracted_articles = [x, y]
logger.info(" -- Sucessfull scraped mainpages-- ")

#Conect to redisdb and preqesiuts
db = get_db() 

#random_int = 0  #commented out from former version of the script

proxy = choose_proxy_from_proxyrotation(local_request=1,
                                        get_html_via_tor=0,
                                        get_html_via_webscrapingapi=0,
                                        get_html_via_scrapingapi=0)    # load a proxy for consistency of code
backed_arts = []

#TO DO
# - alle states überprüfen
# - picture seiten werden nicht korrekt gesrapped

logger.info("Number of Articles found: {num}".format(num=len(extracted_articles)))

for idx, art in enumerate(extracted_articles):
    print(art)
    proxy = choose_proxy_from_proxyrotation(local_request=1,
                                            get_html_via_tor=0,
                                            get_html_via_webscrapingapi=0,
                                            get_html_via_scrapingapi=0) 
    logger.info("proxy with {s} url".format(s=proxy[1]))

    
    if check_url_exist(db, art['url']) == False:
        
        sleeptime = random.randint(3,10)
        
        logger.info("sleeping {num} secs...".format(num=sleeptime))
        
        time.sleep(sleeptime)
        
        logger.info("Article extracted, used function " + str(proxy[0]))
        
        print(extracted_articles[idx]['url'])
        
        status , extracted_articles = execute_get_request_article(proxy_func = proxy[0],
                                    _url_source=url_source,
                                    article=art,
                                    _db = db,
                                    extracted_articles=extracted_articles,
                                    idx=idx)
        
        if status == 1:
            # Try again, if proxy malfunctioned
            
            proxy = choose_proxy_from_proxyrotation(local_request=1,
                                                    get_html_via_tor=0,
                                                    get_html_via_webscrapingapi=0,
                                                    get_html_via_scrapingapi=0) 
            
            logger.warning("Empty html. Try with new created proxy -" + str(proxy[0]))
            
            status , extracted_articles = execute_get_request_article(proxy_func = proxy[0],
                        _url_source=url_source,
                        article=art,
                        _db = db,
                        extracted_articles=extracted_articles,
                        idx=idx)
            
            if status==1:
                
                logger.error("Still empty html.")
                
            
    else:
        logger.info("url in db found")
    