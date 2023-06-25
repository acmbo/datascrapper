from db.redis_dw import get_dw_article_by_url, REDISDB, get_db, savedb, add_article_hashset
from dw.article_v_02 import extract_article_data
#from dw.article import extract_article_data
from dw.mainpage import get_empty_article_meta_data
from analyzer.arc import Analyzer
from utils.proxy import choose_proxy_from_proxyrotation

import time
import tqdm
from datetime import datetime


# Setup
db = get_db(db_number=REDISDB)
an = Analyzer(REDISDB)

# Get urls and dates
data = an.get_all_keys_with_date()

errors: list = []
new_data = []

GETDATE = False
EXCHANGEDATES = True

print("Start")
for _url, _date in tqdm.tqdm(data):
    
    if EXCHANGEDATES:
        old_art = get_dw_article_by_url(db, _url)
        
        datetime_object = None
        
        try:
            if old_art["Datum"] != "":
                datetime_object = datetime.strptime(old_art["Datum"], '%d.%m.%Y')
        except Exception as e:
            try:
                datetime_object = datetime.strptime(old_art["Datum"], '%Y-%m-%d')
                old_art["Datum"] = datetime.strftime(datetime_object , '%d.%m.%Y')
                add_article_hashset(db, old_art)
            #add_article_hashset(db, d[1])
            except Exception as ex:
                print(ex)

    
    if GETDATE:
        if _date == "":

            choosen_proxy = choose_proxy_from_proxyrotation()
            html = choosen_proxy[0]("https://www.dw.com" + _url)
      
            
            if html:
          
                empty_art = get_empty_article_meta_data()
       
                filled_art = extract_article_data(empty_art, html)
       
                old_art = get_dw_article_by_url(db, _url)
                
                for key, val in old_art.items():
                    if val == "":
                        old_art[key] = filled_art[key]
                    #if filled_art[key] == "":pass
                        #print("Still Empty")
                new_data.append((_url, old_art))
       
                #print("sleep")
                time.sleep(3)
                
            else:
                errors.append(_url)

for d in new_data:
    if GETDATE:
        if d[1]["Datum"]!= "":
            add_article_hashset(db, d[1])
		
#get_dw_article_by_url(db, url)
savedb(db)
