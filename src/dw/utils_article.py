"""Helperfunctions to process extracetd article meta data"""

from dw.mainpage import get_empty_article_meta_data

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
        
    
    