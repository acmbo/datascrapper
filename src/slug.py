import datetime
import time
import random
from utils.proxy import choose_proxy_from_proxyrotation
from scrape_dw import scrape_dw_theme_page
from dw.utils_article import remove_double_entrys_in_article
from dw.article import extract_article_data
from db.dw_db import get_db, add_article, check_url_exist


def float_to_timeformat_of_day(random_time_of_day: float):
    """Converts a float between 0 and 24 to timeformat of hour,minutes,seconds

    Args:
        random_time_of_day (float): float between 0 and 24

    Returns:
        (tuple): hour in int , minutes in int, seconds in int
    """
    # check for good input
    if random_time_of_day < 24:
        
        hour = int(random_time_of_day)
        
        if hour > 0:
            minutes = int(random_time_of_day % hour * 60)
        else:
            minutes = int(random_time_of_day * 60)
        
        if minutes >0:
            seconds = int(random_time_of_day % hour * 60  % minutes * 60)
        else:
            seconds = int(random_time_of_day % hour * 60  % minutes * 60)
        
        return hour, minutes,seconds 
    
    else:
        print("Error in Function: to high float (24=<..) as input")
        return (0,0,0)
     


def select_random_time_of_a_day(**kwargs):
    """Creates random time of the day. Through **kwargs hour, minutes or seconds can be 
    set individualy on calling the function

    Returns:
        (tuple): CostumTime Tuple with hour, minute and seconds as attribute
    """
    
    from collections import namedtuple
    
    CustomTime = namedtuple('CustomTime', 'hour minute seconds')
    
    random_time_of_day = random.random()*24   #random.random creates in intervall of [0,1)
    
    hour, minutes, seconds = float_to_timeformat_of_day(random_time_of_day)
    
    #set variable to inputs, if costumizable time is wanted
    for key, value in kwargs.items():
        if key =="hour":
            hour = value
        elif key =="minutes":
            minutes = value
        elif key == "seconds":
            seconds = value
        else:
            continue

    return CustomTime(hour=hour, minute=minutes, seconds=seconds)
    

def get_actual_datetime():
    return datetime.datetime.now()


def time_is_passed_by_actualTime(timepoint: tuple):
    """Checks if minutes and houres of timpoint have passed the current time

    Args:
        timepoint (customtimetuple): time tuple generated by select_random_time_of_a_day() function

    Returns:
        (bool): if houre and minutes of timepoint are bigger then current Time
    """
    actual_time = get_actual_datetime()
    return actual_time.hour >= timepoint.hour and actual_time.minute >= timepoint.minute           
    

def check_change_of_day_in_datetimevalues(newer_datetimevalue, old_datetimevalue):
    """Checks if a day has passed. Acesses calender representation of time and not the
    true timedelta

    Args:
        newer_datetimevalue (datetime): the newer time value as datettime.datetime
        old_datetimevalue (datetime): the older time value as datetime.datetime

    Returns:
        (bol): changes within days
    """
    day_value_delta = newer_datetimevalue.day - old_datetimevalue.day
    
    if -1 < day_value_delta < 1:
        return False # Same Day
    if day_value_delta >= 1:
        return True # new day
    if day_value_delta <= -1:
        return True # old day


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
        choosen_proxy = choose_proxy_from_proxyrotation()
        run=True
        
        while run:
            print("sleeping...")
            time.sleep(random.randint(10,30))
            
            print("scraping")
            html = choosen_proxy[0](url)  
            
            if html:  
                extracted_articles.extend(scrape_dw_theme_page(html))
                run=False
            else:
                print("ERROR:Couldnt extract page")
    
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

    return extracted_articles



def crawl_dw():
    """crwals dw front page and article pages and add articles as html and textformat to a mongodb
    """
    
    url_source = "https://www.dw.com/"     # Needed fpr building hrefs-urls

    extracted_articles = get_dw_front_pages_data()

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
        print("proxy with {s} url".format(s=proxy[1]))
        
        if check_url_exist(db,art['url']) == False:
            
            print("sleeping..")
            time.sleep(random.randint(3,10))

            try:
                html = proxy[0](url_source + art['url'])
                extracted_articles[idx] = preprocess_meta_data(extract_article_data(art, html))
                add_article(db, extracted_articles[idx])
                print("Article extracted, used function " + str(proxy[0]))
            
            except:
                print("error")
                
        else:
            print("url in db found")
    

if __name__ == "__main__":

    TIME = get_actual_datetime()
    LASTACTIVETIME = get_actual_datetime()
    NEWDAY = check_change_of_day_in_datetimevalues(TIME,LASTACTIVETIME)
    STARTHOUR = int(20+random.random()*4)
    STARTTIMEONNEWDAY = select_random_time_of_a_day(hour=STARTHOUR)
    print(STARTHOUR)
    print(STARTTIMEONNEWDAY)

    GLOBAL_RUN = True



    while GLOBAL_RUN:

        TIME = get_actual_datetime()    
        NEWDAY = check_change_of_day_in_datetimevalues(TIME,LASTACTIVETIME)
        
        if NEWDAY and time_is_passed_by_actualTime(STARTTIMEONNEWDAY):
            
            crawl_dw()
            
            LASTACTIVETIME = get_actual_datetime()
            
            # Data for next run
            STARTHOUR = int(20+random.random()*4)
            STARTTIMEONNEWDAY = select_random_time_of_a_day(hour=STARTHOUR)


            
    
    
