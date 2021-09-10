"""
Functions for extracting infromation from Mainpage.
Creates Dictionarys from Teaser data of dw.com/de.
Needs HTMl Input from BS4 Python to run.

"""

from bs4 import element             # Import for Documentation purposes



def get_empty_article_meta_data():
    """returns dictionary for meta data storage of article

    Returns:
        dict: meta data dictionary of article
    """
    dict_article_structure = {
    'url':'',
    'title':'',
    'subtitle':'',
    'abstract':'',
    'image_title': '',
    'mainarticle': False,
    'video': False,
    'meistgelesen':False,
    'redaktionsempfehlung':False,
    'Datum':'',
    'Autorin/Autor':'',
    'Permalink':'',
    'Themenseiten':'',
    'Schlagwörter':'',
    'Artikel':'',
    }
    return dict_article_structure.copy()


def find_term_in_bstag_attr(tags: element.ResultSet, search_in_attr: str = 'id', searchterm: str = 'bodyContent'):
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


def partialfind_term_in_bstag_attr(tags: element.ResultSet, search_in_attr: str = 'id', searchterm: str = 'bodyContent'):
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
                
                if type(tag.attrs[search_in_attr]) == str:
                    
                     if searchterm in tag.attrs[search_in_attr]:
                        result.append(tag)
                    
                elif type(tag.attrs[search_in_attr]) == list:
                    
                    if True in [term.__contains__(searchterm) for term in tag.attrs[search_in_attr]]:           
                        #if searchterm in tag.attrs[search_in_attr]:
                        result.append(tag)
                else:
                    raise ValueError()
                    
        except Exception as error:
            raise Exception('Error encounterd while searching for tags: {s}'.format(s=error))
    
    return result  



def extract_main_article_meta(mainarticle_hrefs: element.ResultSet):
    """Extracts Data from mainarticle html element.

    Args:
        mainarticle_hrefs (element.ResultSet): Resultset from bs4, which has meta data about mainarticle
    """
    
    foundarticles = []
    
    for part in mainarticle_hrefs:
        
        dict_mainarticle = get_empty_article_meta_data()

        try:
            if dict_mainarticle['url'] != part['href'] and part['href'] != '':
                dict_mainarticle['url'] = part['href']
        except:
            dict_mainarticle['url'] = dict_mainarticle['url']
        
        try:
            token = part.find("img")['title']
            if dict_mainarticle['title'] != token and token != '':
                dict_mainarticle['title'] = token
                
        except:
            dict_mainarticle['title'] = dict_mainarticle['title']
        
        try:
            token = part.find("h4").text
            if dict_mainarticle['subtitle'] != token and token != '':
                dict_mainarticle['subtitle'] = part.find("h4").text
        except:
            dict_mainarticle['subtitle'] = dict_mainarticle['subtitle']
        
        try:
            if part.find("h2").text:
                dict_mainarticle['subtitle'] += part.find("h2").text
        except:
            dict_mainarticle['subtitle'] = dict_mainarticle['subtitle']
        
        try:
            token = part.find("p").text
            if dict_mainarticle['abstract'] != token and token != '':
                dict_mainarticle['abstract'] = token
        except:
            dict_mainarticle['abstract'] = dict_mainarticle['abstract']
        
        dict_mainarticle['mainarticle'] = True
        
        foundarticles.append(dict_mainarticle.copy())    # Deepcopy for ensuring you create independend copy
        
    return foundarticles





def extract_basic_article_meta(article_hrefs: element.ResultSet):
    """Extracts Data from mainarticle html element.

    Args:
        article_hrefs (element.ResultSet): Resultset from bs4, which has meta data about mainarticle
    """
        
    foundarticles = []
    
    for part in article_hrefs:
  
        dict_article = get_empty_article_meta_data()
        
        try:
            token = part.find('a')['href']
            if dict_article['url'] != token and token != '':
                dict_article['url'] = token
        except:
            dict_article['url'] = dict_article['url']
        
        try:
            token = part.find("img")['title'].text
            if dict_article['image_title'] != token and token != '':
                dict_article['title'] = token
                
        except:
            dict_article['image_title'] = dict_article['image_title']
        
        try:
            token = part.find('h2')
            if dict_article['title'] != token and token != '':
                dict_article['title'] = token
        except:
            dict_article['title'] = dict_article['title']
               
        try:
            token = part.find("p").text
            if dict_article['abstract'] != token and token != '':
                dict_article['abstract'] = token
        except:
            dict_article['abstract'] = dict_article['abstract']
        
        foundarticles.append(dict_article.copy())   #deepcopy for ensuring you create new copy
        
    return foundarticles
