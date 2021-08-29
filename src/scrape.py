"""
Scraper for DW.de Website to collect news articel data in german

"""

from urllib.request import urlopen
from bs4 import BeautifulSoup


def find_term_in_bstag_attr(tags, search_in_attr: str = 'id', searchterm: str = 'bodyContent'):
    """Searchfunction for searching within attributes of a set of tags found in html through beatifull soup.
       Returns a list of tags, which have the attribute from "search in attr" with value from "searchterm"
    Args:
        tags (bs4.element.Resultset): list of tags from bs4.find_all(), e.g tag = soup.find_all("div")
        search_in_attr (str, optional): key/name of attribte to look for. Defaults to 'id'.
        searchterm (str, optional): Values of attribute, to look for. Defaults to 'bodyContent'.
    """
    
    result = []
    
    for tag in tags:
        
        try:                # try to acces attributes dictionary
            if search_in_attr in tag.attrs.keys():
                
                if tag.attrs[search_in_attr] == searchterm:
                    result.append(tag)
                    
        except Exception as error:
            raise Exception('Error encounterd while searching for tags: {s}'.format(s=error))
    
    return result  


def partialfind_term_in_bstag_attr(tags, search_in_attr: str = 'id', searchterm: str = 'bodyContent'):
    """Searchfunction for searching within attributes of a set of tags found in html through beatifull soup.
       Returns a list of tags, which have the attribute from "search in attr" with value from "searchterm"
       
       Searches with partial string matching.
       
    Args:
        tags (bs4.element.Resultset): list of tags from bs4.find_all(), e.g tag = soup.find_all("div")
        search_in_attr (str, optional): key/name of attribte to look for. Defaults to 'id'.
        searchterm (str, optional): Values of attribute, to look for. Defaults to 'bodyContent'.
    """
    
    result = []
    
    for tag in tags:
        
        try:                # try to acces attributes dictionary
            if search_in_attr in tag.attrs.keys():
                
                if searchterm in tag.attrs[search_in_attr]:
                    result.append(tag)
                    
        except Exception as error:
            raise Exception('Error encounterd while searching for tags: {s}'.format(s=error))
    
    return result  


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

    body_parts = find_term_in_bstag_attr(divs, search_in_attr='id', searchterm='bodyContent')

    body = body_parts[0]
    divs_body = body.find_all("div")


    articles = []

    #get Mainarticle
    mainarticle = find_term_in_bstag_attr(divs_body, search_in_attr='class', searchterm=['col4a'])

    # search for content
    mainarticle = mainarticle[0]
    mainarticle_hrefs = mainarticle.find_all("a", href=True)
    
    dict_mainarticle = {
        'url':'',
        'title':'',
        'subtitle':'',
        'abstract':'',
        'mainarticle': True
    }
    
    for part in mainarticle_hrefs:
        
        try:
            if dict_mainarticle['url'] != part['href'] and part['href'] != '':
                dict_mainarticle['url'] = part['href']
        except:
            dict_mainarticle['url'] = dict_mainarticle['url']
        
        try:
            if dict_mainarticle['title'] != part.find("img")['title'] and part.find("img")['title'] != '':
                dict_mainarticle['title'] = part.find("img")['title']
                print(part.find("img")['title'])
        except:
            dict_mainarticle['title'] = dict_mainarticle['title']
        
        try:
            if dict_mainarticle['subtitle'] != part.find("h4").text and part.find("h4").text != '':
                dict_mainarticle['subtitle'] = part.find("h4").text
        except:
            dict_mainarticle['subtitle'] = dict_mainarticle['subtitle']
        
        try:
            if part.find("h2").text:
                dict_mainarticle['subtitle'] += part.find("h2").text
        except:
            dict_mainarticle['subtitle'] = dict_mainarticle['subtitle']
        
        try:
            if dict_mainarticle['abstract'] != part.find("p").text and part.find("p").text != '':
                dict_mainarticle['abstract'] = part.find("p").text
        except:
            dict_mainarticle['abstract'] = dict_mainarticle['abstract']
            
    articles.append(dict_mainarticle)
    
    site_div_elements = partialfind_term_in_bstag_attr(divs_body, search_in_attr='class', searchterm='basicTeaser')

        
