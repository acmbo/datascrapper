"""
Scraper for DW.de Website to collect news articel data in german

"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4 import element             # Import for Documentation purposes
from dw.mainpage import find_term_in_bstag_attr, partialfind_term_in_bstag_attr, \
                        extract_basic_article_meta, extract_main_article_meta,\
                        get_empty_article_meta_data
                        
from dw.utils_article import remove_double_entrys_in_article, add_value_to_article_key,\
                            check_ref_is_a_dwhomepage


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



def get_all_hrefs_from_page(soup, add_root_page: str = ""):
    """Returns a list of urls ready for use

    Args:
        soup (bs4.soup): soup of html

    Returns:
        list: list of urls
    """
    # get all links
    hrefs = [link.get('href') for link in soup.find_all('a') ]
    # Removes external links
    hrefs = [href for href in hrefs if href != '' and href != None and href[0] == "/"]
    #adds a root page to all hrefs
    if add_root_page != "":
        hrefs = [add_root_page + href for href in hrefs]
        
    hrefs = list(dict.fromkeys(hrefs)) # remove duplicates
    
    hrefs = [href for href in hrefs if href.split("/")[1] == "de"]
    
    return hrefs



def scrape_dw_theme_page(html:str):
    """Scrapes a theme/main page of dw and returns list of found articles

    Args:
        html (str): html text of the website as string
        url (str): url of theme page
        url_source (str): base of url of dw.com for constructing further child urls

    Returns:
        (list) : list of article meta data dictinionarys
    """


    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all("div")

    #Get Main Body
    body_parts = find_term_in_bstag_attr(divs, search_in_attr='id', searchterm='bodyContent')
    body = body_parts[0]
    divs_body = body.find_all("div")


    #For collecting data
    articles = []
    hrefs = []

    #Get all hrefs from website
    hrefs = get_all_hrefs_from_page(soup)
    
    # Extract metadata from mainarticle
    mainarticle = find_term_in_bstag_attr(divs_body, search_in_attr='class', searchterm=['col4a'])

    if len(mainarticle) > 0: 
        mainarticle = mainarticle[0]
        mainarticle_hrefs = mainarticle.find_all("a", href=True)
        
        dict_mainarticle = extract_main_article_meta(mainarticle_hrefs)
        articles.extend(dict_mainarticle)
        
    #Get Basic Teasers
    site_div_elements = partialfind_term_in_bstag_attr(divs_body, search_in_attr='class', searchterm='basicTeaser')
    site_articles = extract_basic_article_meta(site_div_elements)
    articles.extend(site_articles)
        

    #Untere Newsbalken
    autTop_div_elements = partialfind_term_in_bstag_attr(divs_body, search_in_attr='class', searchterm='autoTopicTeaser')
    hrefs.extend(get_hrefs_of_tags(autTop_div_elements))


    #Redaktionsempfehlung
    artDetT_div_elements = partialfind_term_in_bstag_attr(divs_body, search_in_attr='class', searchterm='articleDetailTeaser')
    redaktions_empfehlungen = get_hrefs_of_tags(artDetT_div_elements)
    hrefs.extend(redaktions_empfehlungen)

    #Am meisten gelesen
    contentListTeaser = partialfind_term_in_bstag_attr(divs_body, search_in_attr='class', searchterm='articleDetailTeaser')
    meistgelesen = get_hrefs_of_tags(contentListTeaser)
    hrefs.extend(meistgelesen)

    hrefs = list(set(hrefs))
    hrefs = [href for href in hrefs if not check_ref_is_a_dwhomepage(href)]
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
    
    # add Todays date
    from datetime import datetime
    for art in articles:
        
        art['scrapedate'] = datetime.now().isoformat()
    
    return articles
    
    
if __name__ == '__main__':
    
    url_source = "https://www.dw.com/"     # Needed fpr building hrefs-urls
    url = "https://www.dw.com/de/"
    #url = "https://www.dw.com/de/themen/welt/s-100029"
    
    page = urlopen(url)

    html_bytes = page.read()
    html = html_bytes.decode("utf_8")

    #get Title
   
    articles = scrape_dw_theme_page(html)
    
    