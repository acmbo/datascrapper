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
empty_entrys = 0
correct_entrys = 0
 
for key in ['url', 'title', 'subtitle', 'abstract', 'image_title', 'mainarticle', 'video', 'meistgelesen', 'redaktionsempfehlung', 'Datum', 'Autorin/Autor', 'Permalink', 'Themenseiten', 'Schlagwörter', 'Artikel']:
    if key == 'url':
        if type(test[key]) == str:
            correct_entrys += 1
        else:
            empty_entrys +=1 
    if key == 'title':
        if type(test[key]) == str:
            correct_entrys += 1
        else:
            empty_entrys +=1 
    if key == 'subtitle':
        if type(test[key]) == str:
            correct_entrys += 1
        else:
            empty_entrys +=1 
    if key == 'abstract':
        if type(test[key]) == str:
            correct_entrys += 1
        else:
            empty_entrys +=1 
    if key == 'image_title':
        if  type(test[key]) == str:
            correct_entrys += 1
        else:
            empty_entrys +=1 
    if key == 'mainarticle':
        if type(test[key]) == bool:
            correct_entrys += 1
        else:
            empty_entrys +=1 
    if key == 'video':
        if type(test[key]) == bool:
            correct_entrys += 1
        else:
            empty_entrys +=1 
    if key == 'meistgelesen':
        if type(test[key]) == bool:
            correct_entrys += 1
        else:
            empty_entrys +=1 
    if key == 'redaktionsempfehlung':
        if type(test[key]) == bool:
            correct_entrys += 1
        else:
            empty_entrys +=1 
    if key == 'Datum':
        if type(test[key]) == str:
            correct_entrys += 1
        else:
            empty_entrys +=1 
    if key == 'Autorin/Autor':
        if type(test[key]) == str:
            correct_entrys += 1
        else:
            empty_entrys +=1 
    if key == 'Permalink':
        if type(test[key]) == str:
            correct_entrys += 1
        else:
            empty_entrys +=1 
    if key == 'Themenseiten':
        if type(test[key]) == list:
            correct_entrys += 1
        else:
            empty_entrys +=1 
    if key == 'Schlagwörter':
        if type(test[key]) == list:
            correct_entrys += 1
        else:
            empty_entrys +=1 
    if key == 'Artikel':
        if type(test[key]) == dict:
            correct_entrys += 1
        else:
            empty_entrys +=1 
            
print("Correct Entrys: ", correct_entrys)
print("Empty Entrys: ", empty_entrys)