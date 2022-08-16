from db.redis_dw import get_dw_article_by_url, REDISDB, get_db, savedb, add_article_hashset
from dw.article_v_02 import extract_article_data
from dw.article import extract_article_data
from dw.mainpage import get_empty_article_meta_data
from analyzer.arc import Analyzer
import requests
import time
import tqdm
# Setup
db = get_db(db_number=REDISDB)
an = Analyzer(REDISDB)

# Get urls and dates
data = an.get_all_keys_with_date()

errors: list = []
new_data = []

for _url, _date in tqdm.tqdm(data):
	if _date == "":
		r = requests.get("https://www.dw.com" + _url)
		
		if r.status_code == 200:
			empty_art = get_empty_article_meta_data()
			html = r.text
			filled_art = extract_article_data(empty_art, html)
			old_art = get_dw_article_by_url(db, _url)
			
			for key, val in old_art.items():
				if val == "":
					old_art[key] = filled_art[key]
				if filled_art[key] == "":
					print("Still Empty")
			new_data.append((_url, old_art))
			print("sleep")
			time.sleep(3)
			
		else:
			errors.append(_url)

get_dw_article_by_url(db, url)
add_article_hashset(db, article)