from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4 import element 
from dw.mainpage import partialfind_term_in_bstag_attr


def get_article_text(longtext: element.ResultSet):
    """Extracts Text from a list of tags. Ignores divs and just includes [h,p] html tags

    Args:
        longtext (bs4.element.tag): bs4.element tags to scrape text from

    Returns:
        (str): joint text
    """
    # Extract Text from list of tags
    text_list = []
    
    for tag in longtext:
        
        if tag.name != 'div':

            if tag.name == 'p':
                try:
                    text_list.append(tag.text)
                except:
                    pass
            else:
                text_list.append(str(tag)) 
                
    text_list = [elem.replace(' ','\n') if elem == ' ' else elem for elem in text_list]
    
    #Fuse text parts into string and returns it
    return ' '.join(text_list)




def extract_article_data(article: dict, url_source: str):    
    
    
    #Get Website HTML  
    new_url_string = url_source + article['url'][1:]
    #new_url_string = new_url_string.encode('utf-8')
    new_url_string = new_url_string.encode("ascii",'ignore')
    page = urlopen(new_url_string.decode('ascii'))

    html_bytes = page.read()
    html = html_bytes.decode("utf8")

    #get Title
    html.find("<title>")
    start_index = html.find("<title>") + len("<title>")
    end_index = html.find("</title>")
    title = html[start_index:end_index]     # html title


    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all("div") 
    body = partialfind_term_in_bstag_attr(divs, search_in_attr='id', searchterm='bodyContent')  
    body_divs = body[0].find_all("div")
    
    
    # get sidebar meta data
    meta_data = partialfind_term_in_bstag_attr(body_divs, search_in_attr='class', searchterm='col1')
    
        
    # extract  sidebar meta data
    #   Data from Website:
    #   include = ["Datum","Autorin/Autor","Permalink"]
    #   exclude = ["Drucken",]
    #   special = ["Themenseiten","Schlagwörter"]
    
    include = ["Datum","Autorin/Autor","Permalink"]
    
    for x in meta_data[0].find_all("li"):
        
        header = x.find_all("strong")
        
        if len(header)>0:
            
            key = x.find_all("strong")[0].text
            
            if key in include:
                
                key_name = x.find_all("strong")[0].text
                val = x.text.replace(key_name,'').replace('\n','')
                article[key_name] = val
            
            if key == "Themenseiten":
                
                key_name = x.find_all("strong")[0].text
                val = [(entry.text, entry['href']) for entry in x.find_all("a")]
                article[key_name] = val
            
            if key == "Schlagwörter":

                key_name = x.find_all("strong")[0].text
                val = [entry.text for entry in x.find_all("a")]
                article[key_name] = val
    
    
    # get article body
    _article = partialfind_term_in_bstag_attr(body_divs, search_in_attr='class', searchterm='col3')
    
    #extract article tags
    longtext = partialfind_term_in_bstag_attr(_article[0].find_all('div'), search_in_attr='class', searchterm='longText')
    
    # store text data
    text = {'Text':'',
            'Title':'',
            'Article_Scene':''}
    
    text['Text'] = get_article_text(longtext[0])    # Longtext as tags
            
            
    # Gets more information from text
    childs = _article[0].findChildren()
    parts_seen = 0
    
    for a in childs:
        #if a.name in ['h4','h3','h2','h1','p']:
        #    
        #    print(a)
        #    print(a.text)
        #    print('----------------------------------')
                    
        if a.name == 'h1':
            
            text['Title'] = a.text
            
        if a.name == 'h4':
            
            text['Article_Scene'] = a.text
        
        #if a.name in ['h3','h2','p'] and parts_seen > 1:
        #    
        #    text['Text'] = text['Text'] + '\n ' + str(a.text)
        
        parts_seen += 1
    
    article['Artikel'] = text
    
    return article
    
    
