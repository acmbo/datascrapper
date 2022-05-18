"""utility class and functions for data analysis"""
import sys
from pathlib import Path
from datetime import date, datetime

from sympy import timed

# For dev purposes, so you can find db.redis
path = Path(__file__)
if path.parent.name == 'analyzer':
    sys.path.append(str(path.parents[1]))
    
    
import numpy as np
from db.redis_dw import get_db, get_all_dw_article, get_dw_article_by_url
from db.redis_dw import *

def get_redis_data(db):
    """Generator for returning data from redis db"""
    keys = np.array(get_all_dw_article(db))
    for key in keys:
        #print("KEY: ", key)
        yield get_dw_article_by_url(db, key, hset=True)


class Analyzer:
    """Analyzer Meta Class
    """
    def __init__(self, dbnumber):
        self.used_db = dbnumber
        self.date_today = datetime.today()
        
    
    def connect_to_db(self):
        db = get_db()
        return db
    
    
    def get_all_keys_with_date(self):
        redis_data =   [] # np.array([])
        # Faster to append to list first and convert to numpy array, https://stackoverflow.com/questions/29839350/numpy-append-vs-python-append
        
        with self.connect_to_db() as db:
            for data in get_redis_data(db):
                try: 
                    key=data["url"]
                    val=data["Datum"]
                except:
                    #print("Error on ", data)
                    key = None
                    val = None
                redis_data.append((key, val))
                
        return np.array(redis_data)
    
    
    def get_data_filtered_by_time(self, daydelta: int = None):
        """Get Keys from Redis DB filtered by a time delta. None as daydelta is possible, so you get all keys from db

        Args:
            daydelta (int, optional): Timedelta in days. Defaults to None.

        Returns:
            valid_keys (array): array of tuples of correct keys from db
        """
        
        rd = self.get_all_keys_with_date()

        valid_keys = []
        
        for d in rd:
            if isinstance(d[1], str) and d[1] != "":    # Clean Data for invalid entrys
                #print("KEY: ", d[1])
                datetime_object = datetime.strptime(d[1], '%d.%m.%Y')
                #print(datetime_object)
                timedelta = datetime.today() - datetime_object
                
                if daydelta and timedelta.days < daydelta:
                    valid_keys.append((d[0], datetime_object))
                    
                elif daydelta == None:
                    valid_keys.append((d[0], datetime_object))
                    
        return np.array(valid_keys)
        
    
    
if __name__ =="__main__":
    
    an = Analyzer(1)
    data = an.get_data_filtered_by_time()
    
    import spacy
    sp_sm = spacy.load('de_core_news_sm')
    sp_em = spacy.load('de_dep_news_trf')

    import unicodedata
    
    
    with an.connect_to_db() as db:
        article = get_dw_article_by_url(db, data[5][0], hset=True)
        
    print(article)

    text = unicodedata.normalize("NFKD",article["Artikel"]["Text"])
    text = text.replace("</h2>", "").replace("<h2>", "").replace("\n", "")
    
    def spacy_ner_get_LOC(document,spacy_model):
        return {(ent.text.strip(), ent.label_) for ent in spacy_model(document).ents if ent.label_ in ['LOC', 'GPE'] }
    
    def spacy_ner(document, spacy_model):
        return {(ent.text.strip(), ent.label_) for ent in spacy_model(document).ents}

    
    
    
    sp_em = spacy.load('de_dep_news_trf')
    
    with open("test_article_txt.txt","r") as f:
        test_ar = f.readline()
    
    x = spacy_ner(test_ar, sp_em)
    x = spacy_ner_get_LOC(test_ar, sp_sm)
    
    
    import timeit
    
    s="""\
    x = []
    for i in range(1000):
        x.append(str(i))
    """
    
    timeit.timeit(stmt=s, number=100000, setup ="import numpy as np")

        
    s="""\
    x = np.empty((0,2), str)
    for i in range(1000):
        x=np.append(x, str(i))
    """
        