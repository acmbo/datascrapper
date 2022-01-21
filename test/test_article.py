import os
os.chdir("../src")

import sys
sys.path.append(os.getcwd())
os.chdir("../test")

import pickle
from dw.article import extract_article_data
from dw.mainpage import get_empty_article_meta_data
from utils.proxy import local_request

test_hmtl_file = 'test_html.pickle'
url = "https://www.dw.com/de/vom-gro%C3%9Fen-sport-ins-exil-belarussische-sportler-%C3%BCber-ihr-leben-im-ausland/a-60425937"




if test_hmtl_file in os.listdir():
    with open(test_hmtl_file, 'rb') as handle:
        html = pickle.load(handle)
    
else:
    
    html = local_request(url)

    if html:
        with open(test_hmtl_file, 'wb') as handle:
            pickle.dump(html, handle, protocol=pickle.HIGHEST_PROTOCOL)

art = get_empty_article_meta_data()
art['url'] = url
test = extract_article_data(art, html)

