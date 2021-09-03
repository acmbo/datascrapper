"""
Scraper for DW.de Website to collect news articel data in german

"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4 import element             # Import for Documentation purposes
from dw.mainpage import find_term_in_bstag_attr, partialfind_term_in_bstag_attr, \
                        extract_basic_article_meta, extract_main_article_meta,\
                        get_empty_article_meta_data


def find_double_and_unique_entrys_to_list(list1: list, list2: list):
    """Finds double entry and unique entrys in a list and returns a tuple of both results

    Args:
        list1 (list): list of items
        list2 (list): list of items

    Returns:
        tuple: uniquevales and double values
    """
    unique_vals= []
    double_vals = []

    for item in list1:
        if item not in list2:
            unique_vals.append(item)
        else:
            double_vals.append(item)
            
    return (unique_vals, double_vals)


def get_hrefs_of_tags(article_hrefs: element.ResultSet, html_tag: str ="a"):
    """extracts hrefs from bs4.element

    Args:
        article_hrefs (element.ResultSet): bs4.element containing html

    Returns:
        foundhrefs[list]: list of hrefs
    """
    foundhrefs = []
    
    for tag in article_hrefs:
        
        sub_tags = tag.find_all(html_tag)
        
        for sub_tag in sub_tags:
        
            try:
                foundhrefs.append(sub_tag['href'])
                
            except:
                continue
        
    return foundhrefs


def add_value_to_article_key(articles:list, 
                                key:str, 
                                val, 
                                searchval:str,
                                searchkey:str = 'url'):
    """[summary]

    Args:
        articles (list):list of articles
        key (str): look for key in dictionary of article
        val ([type]): add value to key entry in dictionary article
        searchval (str): search for this value to identify article to add value
        searchkey (str, optional): search at a certain key in article dicitonary.

    Returns:
        list: list of articles
    """
    for article in articles:
        if article[searchkey] == searchval:
            article[key] = val
    return articles


def print_articlesdict_with_some_value(articles, key, check_for_this_val):
    """Helperfunction to print Aricles with some value in their meta data dict.
    e.g: meistegelesen (key) == True (check_for_this_val)

    """
    for art in articles:
        try:
            if art[key]==check_for_this_val:
                print(art)
        except:
            pass


def remove_double_entrys_in_article(articles: list):
    """Removes double articles in list of articles

    Args:
        articles (list): list of articles, which are described as meta_dict of articles

    Returns:
        [tuple]: tuple of the new articles and found double entrys
    """

    seen_articles = []
    seen_hrefs = []
    double_hrefs = []
    indexes_to_remove = []
    new_content = []
    
    
    for i, art in enumerate(articles):
        
        if art['url'] not in seen_hrefs:
            seen_hrefs.append(art['url'])
            seen_articles.append(art)
            
        else:
            idx = seen_hrefs.index(art['url'])
            double_hrefs.append(art['url'])
            indexes_to_remove.extend([i,idx])
            
            replace_dict = get_empty_article_meta_data()
            
            for key in articles[idx].keys():
                #print('{s0}: {s1} {s1}'.format(s1=articles[idx][key],
                #                             s2=art[key],
                #                             s0=key))
                
                
                
                if type(articles[idx][key]) == bool:
                    
                    if articles[idx][key] == True:
                            replace_dict[key] = articles[idx][key]
                    else:
                        replace_dict[key] = art[key]

                else:
                
                    if len(articles[idx][key]) >= len(art[key]):
                        replace_dict[key] = articles[idx][key]
                    else:
                        replace_dict[key] = art[key]
            
            new_content.append(replace_dict)

    
    for i, art in enumerate(articles):
        if i not in indexes_to_remove:
            new_content.append(art)
    
    return new_content, double_hrefs
        
    
    
    
    
if __name__ == '__main__':
    
    url_source = "https://www.dw.com/"     # Needed fpr building hrefs-urls
    url = "https://www.dw.com/de/"
    page = urlopen(url)

    html_bytes = page.read()
    html = html_bytes.decode("utf_8")

    #get Title
    html.find("<title>")
    start_index = html.find("<title>") + len("<title>")
    end_index = html.find("</title>")
    title = html[start_index:end_index]


    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all("div")

    #Get Main Body
    body_parts = find_term_in_bstag_attr(divs, search_in_attr='id', searchterm='bodyContent')
    body = body_parts[0]
    divs_body = body.find_all("div")


    #For collecting data
    articles = []
    hrefs = []
    

    # Extract metadata from mainarticle
    mainarticle = find_term_in_bstag_attr(divs_body, search_in_attr='class', searchterm=['col4a'])
    mainarticle = mainarticle[0]
    mainarticle_hrefs = mainarticle.find_all("a", href=True)
    
    dict_mainarticle = extract_main_article_meta(mainarticle_hrefs)
    articles.extend(dict_mainarticle)
        
    # Get all Types of article classes on Website
    attrib_div=[x.attrs for x in partialfind_term_in_bstag_attr(divs_body, search_in_attr='class', searchterm='easer')]
    print(list(set([y for x in attrib_div for y in x['class']])))
    
    #Get Basic Teasers
    site_div_elements = partialfind_term_in_bstag_attr(divs_body, search_in_attr='class', searchterm='basicTeaser')
    site_articles = extract_basic_article_meta(site_div_elements)
    articles.extend(site_articles)
        

    #Untere Newsbalken
    autTop_div_elements = partialfind_term_in_bstag_attr(divs_body, search_in_attr='class', searchterm='autoTopicTeaser')
    hrefs.extend(get_hrefs_of_tags(autTop_div_elements))
    
    # ImgTeaser sind social Media verlinkungen
    # picTea_div_elements = partialfind_term_in_bstag_attr(divs_body, search_in_attr='class', searchterm='pictureTeaser')
    #hrefs = get_hrefs_of_tags(picTea_div_elements)
    
    #Redaktionsempfehlung
    artDetT_div_elements = partialfind_term_in_bstag_attr(divs_body, search_in_attr='class', searchterm='articleDetailTeaser')
    redaktions_empfehlungen = get_hrefs_of_tags(artDetT_div_elements)
    hrefs.extend(redaktions_empfehlungen)
    
    #Am meisten gelesen
    contentListTeaser = partialfind_term_in_bstag_attr(divs_body, search_in_attr='class', searchterm='articleDetailTeaser')
    meistgelesen = get_hrefs_of_tags(contentListTeaser)
    hrefs.extend(meistgelesen)
    
    hrefs = list(set(hrefs))
    extracted_hrefs = [article['url'] for article in articles]
         
    unique_hrefs, double_hrefs = find_double_and_unique_entrys_to_list(hrefs, extracted_hrefs) 
    
    #adding new found hrefs to articles list
    for href in unique_hrefs:
        new_article_meta = get_empty_article_meta_data()
        new_article_meta['url'] = href
        articles.append(new_article_meta)
        
        
    for href in meistgelesen:
        articles = add_value_to_article_key(articles, 
                                'meistgelesen', 
                                val = True, 
                                searchval = href,
                                searchkey = 'url')
    
    for href in redaktions_empfehlungen:
        articles = add_value_to_article_key(articles, 
                            'redaktionsempfehlung', 
                            val = True, 
                            searchval = href,
                            searchkey = 'url')
    
    #Remove double articles
    new_content, double_hrefs = remove_double_entrys_in_article(articles)










    articles = new_content
    
    import time
    
    for i in range(0,5):
        

        time.sleep(2)
        continue
    
    i=0
    articles[i]['url']   
    new_url_string = url_source + articles[i]['url'][1:]
    #new_url_string = new_url_string.encode('utf-8')
    new_url_string = new_url_string.encode("ascii",'ignore')
    page = urlopen(new_url_string.decode('ascii'))

    html_bytes = page.read()
    html = html_bytes.decode("utf8")

    #get Title
    html.find("<title>")
    start_index = html.find("<title>") + len("<title>")
    end_index = html.find("</title>")
    title = html[start_index:end_index]


    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all("div") 
    body = partialfind_term_in_bstag_attr(divs, search_in_attr='id', searchterm='bodyContent')  
    body_divs = body[0].find_all("div")
    
    meta_data = partialfind_term_in_bstag_attr(body_divs, search_in_attr='class', searchterm='col1')
    
        
        
        
        
    include = ["Datum","Autorin/Autor","Permalink"]
    exclude = ["Drucken",]
    special = ["Themenseiten","Schlagwörter"]
    
    for x in meta_data[0].find_all("li"):
        
        header = x.find_all("strong")
        
        if len(header)>0:
            key = x.find_all("strong")[0].text
            
            if key in include:
                key_name = x.find_all("strong")[0].text
                val = x.text.replace(key_name,'').replace('\n','')
                articles[i][key_name] = val
                
                print(key_name)
                print(val)
                print('-----------')
            
            if key == "Themenseiten":
                
                key_name = x.find_all("strong")[0].text
                val = [(entry.text, entry['href']) for entry in x.find_all("a")]
                articles[i][key_name] = val
            
            if key == "Schlagwörter":

                key_name = x.find_all("strong")[0].text
                val = [entry.text for entry in x.find_all("a")]
                articles[i][key_name] = val
                
    body = body[0]
    
                
                                

        
        
   

    