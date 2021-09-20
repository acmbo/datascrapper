import datetime
import time
import random
from utils.proxy import proxy_rotation
from scrape_dw import scrape_dw_theme_page
from dw.utils_article import remove_double_entrys_in_article
from dw.article import extract_article_data
from db.dw_db import get_db, add_article, check_url_exist


def preprocess_meta_data(article):
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


url_source = "https://www.dw.com/"     # Needed fpr building hrefs-urls
urls = ["https://www.dw.com/de/",
        "https://www.dw.com/de/themen/wissen-umwelt/s-12296",
        "https://www.dw.com/de/themen/kultur/s-1534",
        "https://www.dw.com/de/themen/sport/s-12284",
        "https://www.dw.com/de/themen/welt/s-100029"]


extracted_articles = []


for url in urls:
    #get random proxy
    proxy = proxy_rotation()
    run=True
    
    while run:
        print("sleeping...")
        time.sleep(random.randint(10,30))
        
        print("scraping")
        html = proxy[0](url)  
        
        if html:  
            extracted_articles.extend(scrape_dw_theme_page(html))
            run=False
        else:
            print("ERROR:Couldnt extract page")
        
#Remove double entrys
extracted_articles, double_hrefs = remove_double_entrys_in_article(extracted_articles)

#Conect to mongodb and preqesiuts
db = get_db() 
random_int = 0 
proxy = proxy_rotation()    # load a proxy for consistency of code
backed_arts = []





#TO DO
# - alle states überprüfen
# - picture seiten werden nicht korrekt gesrapped


for idx, art in enumerate(extracted_articles):
    

    if random_int == 0:
        
        proxy = proxy_rotation()
        print("proxy with {s} url".format(s=proxy[1]))
        #if proxy can work with 1 url, if yes extract html
        #if proxy[1] == 1:
            
        print("state 1")
        
        if check_url_exist(db,art['url']) == False:
            
            time.sleep(random.randint(3,10))

            
            try:
                html = proxy[0](url_source + art['url'])
                #
                extracted_articles[idx] = preprocess_meta_data(extract_article_data(art, html))
                add_article(db, extracted_articles[idx])
                print("used function " + str(proxy[0]))
            except:
                print("error")
        else:
            print("url in db found")
        
        #else:      
        #    print("state 4")
        #    random_int = random.randint(2,10)
        #    backed_arts.append((art,idx))
    
    """
    #####muss geprüft werden!
    elif len(backed_arts)==random_int:
        
        print("state 3")
        
        try:
            time.sleep(random.randint(3,10))
    
            list_of_html = proxy[0](url_source + sub_url[0]["url"] for sub_url in backed_arts)
            
            for extraced_solo_article, backed_art in zip(list_of_html, backed_arts):
                extracted_articles[backed_arts[1]] = preprocess_meta_data(extract_article_data(backed_arts[0], extraced_solo_article))
                add_article(db, extracted_articles[backed_arts[1]])
            
        except:
            print("error " + str(random_int))
        
        #restore default status
        random_int = 0
        backed_arts = []
            
    elif len(backed_arts) < random_int and random_int > 0:
        print("state 2")
        backed_arts.append(art)
    """
        
            
