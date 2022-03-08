import time
import random
from utils.proxy import choose_proxy_from_proxyrotation
from utils.time import time_is_passed_by_actualTime, \
    select_random_time_of_a_day, get_actual_datetime, check_change_of_day_in_datetimevalues
from utils.loggers import createStandardLogger    
from scrape_dw import scrape_dw_theme_page
from dw.utils_article import remove_double_entrys_in_article
from dw.article import extract_article_data
#from db.mongo import get_db, add_article, check_url_exist
from db.redis_dw import get_db, add_article_hashset, check_url_exist


logger = createStandardLogger(__name__)


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
            
            logger.info("sleeping...")
            
            time.sleep(random.randint(5,10))
            
            choosen_proxy = choose_proxy_from_proxyrotation()
            
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
            "https://www.dw.com/de/themen/welt/s-100029"]



    extracted_articles = extract_articles_from_urlist_of_dw_theme_pages(urls)
            
            
    #Remove double entrys
    extracted_articles, double_hrefs = remove_double_entrys_in_article(extracted_articles)

    logger.info("Finished Extraction")

    return extracted_articles



def crawl_dw():
    """crwals dw front page and article pages and add articles as html and textformat to a mongodb
    """
    
    logger.info("Start new Crawl")
    
    url_source = "https://www.dw.com/"     # Needed fpr building hrefs-urls

    extracted_articles = get_dw_front_pages_data()
    logger.info(" -- Sucessfull scraped mainpages-- ")

    #Conect to mongodb and preqesiuts
    db = get_db() 

    #random_int = 0  #commented out from former version of the script

    proxy = choose_proxy_from_proxyrotation()    # load a proxy for consistency of code
    backed_arts = []

    #TO DO
    # - alle states überprüfen
    # - picture seiten werden nicht korrekt gesrapped
    
    for idx, art in enumerate(extracted_articles):
        
        proxy = choose_proxy_from_proxyrotation() 
        logger.info("proxy with {s} url".format(s=proxy[1]))
    
        
        if check_url_exist(db,art['url']) == False:
            
            #logger.info("sleeping..")
            #time.sleep(random.randint(3,10))
            logger.info("Article extracted, used function " + str(proxy[0]))
            
            print(idx)
            print(extracted_articles[idx])
            
            try:
                html = proxy[0](url_source + art['url'])
                extracted_articles[idx] = preprocess_meta_data(extract_article_data(art, html))
                add_article_hashset(db, extracted_articles[idx])
                logger.info(" -- Sucessfull scraped {url} -- ".format(url=url_source + art['url']))
                
            except Exception as e:
                logger.error("Error in Slug: {url} = \n {e} ".format(e=e,
                                                                     url=str(url_source + art['url'])))
                
        else:
            logger.info("url in db found")
        
    logger.info("End of Crawl")
    

if __name__ == "__main__":

    TIME = get_actual_datetime()
    LASTACTIVETIME = get_actual_datetime()
    NEWDAY = True
    STARTHOUR = int(20+random.random()*4)
    #STARTHOUR = 13
    STARTTIMEONNEWDAY = select_random_time_of_a_day(hour=STARTHOUR,
                                                    )
                            

    GLOBAL_RUN = True

    while GLOBAL_RUN:
        
        crawl_dw()

        TIME = get_actual_datetime()    
        
        if NEWDAY and time_is_passed_by_actualTime(STARTTIMEONNEWDAY):
            
            crawl_dw()
            
            LASTACTIVETIME = get_actual_datetime()
            
            # Data for next run
            STARTHOUR = int(20+random.random()*4)
            STARTTIMEONNEWDAY = select_random_time_of_a_day(hour=STARTHOUR)
        
        NEWDAY = check_change_of_day_in_datetimevalues(TIME,LASTACTIVETIME)

