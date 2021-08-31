"""
Scraper for DW.de Website to collect news articel data in german

"""


from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4 import element             # Import for Documentation purposes
from dw.mainpage import find_term_in_bstag_attr, partialfind_term_in_bstag_attr, \
                        extract_basic_article_meta, extract_main_article_meta



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


if __name__ == '__main__':
    
    url_source = "https://www.dw.com/"     # Needed fpr building hrefs-urls
    url = "https://www.dw.com/de/"
    page = urlopen(url)

    html_bytes = page.read()
    html = html_bytes.decode("utf8")

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


    articles = []
    

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
        

    autTop_div_elements = partialfind_term_in_bstag_attr(divs_body, search_in_attr='class', searchterm='autoTopicTeaser')
    hrefs = get_hrefs_of_tags(autTop_div_elements)
    
    # ImgTeaser sind social Media verlinkungen
    # picTea_div_elements = partialfind_term_in_bstag_attr(divs_body, search_in_attr='class', searchterm='pictureTeaser')
    #hrefs = get_hrefs_of_tags(picTea_div_elements)
    
    #Redaktionsempfehlung
    artDetT_div_elements = partialfind_term_in_bstag_attr(divs_body, search_in_attr='class', searchterm='articleDetailTeaser')
    
    