from random import randint
import requests
import time 
from bs4 import BeautifulSoup as bs

SLEEPTIME = randint(3,10)

def get_ready_soup_html(url:str):
    """_summary_

    Args:
        url (str):str of url

    Returns:
        soup: soup of beatiful soup, ready html for further analysis
    """
    try:
        req =  requests.get(url)
        soup = bs(req.text)
        return soup
    
    except Exception as e:
        print("ERROR: ", e)
        return None


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
    hrefs = [href for href in hrefs if href[0] == "/"]
    #adds a root page to all hrefs
    if add_root_page != "":
        hrefs = [add_root_page + href for href in hrefs]
    return hrefs


def check_html_for_reuters_site_type(soup, s_type = "article"):
    """Checks if html is a article by defintion of reuters page.
    Known types:
    -article
    -article:section

    Args:
        soup (bs4.soup): soup of html

    Returns:
        bool: true if article
    """
    for findings in soup.head.find_all("meta", {"property":"og:type"}):
        if "content" in findings.attrs.keys():
            if s_type == findings["content"]:
                return True
    return False


def get_empty_article_data_dict():
    
    article_data = {
        "r_site_type":"",
        "url":"",
        "title":"",
        "urls":""
    }
    return article_data


def get_content(soup, tag: str, props: dict):
    """get content from a bs4 query. 
    Query example: soup.head.find("meta", {"property":"og:type1"})

    Args:
        soup (bs4.soup): soup of html
        tag (str): html tag
        porps (dict): propetry to search for

    Returns:
        str: content as string
    """
    if soup.head.find(tag, props):
        
        if "content" in soup.head.find(tag, props).attrs:
            return soup.head.find(tag, props)["content"]
    return ""


def get_page_data(soup):
    """Extracts data from website

    Args:
        soup (bs4.soup): soup of html

    Returns:
        dict: article data as ditcionary
    """
    article_data = get_empty_article_data_dict()

    # Check for page type
    if check_html_for_reuters_site_type(soup,s_type="article"):
        article_data["r_site_type"] = "article"
        article_data["sitetitle"] = soup.title
        article_data["description"] = get_content(soup, "meta",  {"property":"og:description"})
        article_data["published_time"] = get_content(soup, "meta",  {"name":"article:published_time"})
        article_data["modified_time"] = get_content(soup, "meta",  {"name":"article:modified_time"})
        article_data["author"] = get_content(soup, "meta",  {"name":"article:author"})
        article_data["section"] = get_content(soup, "meta",  {"name":"article:section"})
        article_data["page_layout"] = get_content(soup, "meta",  {"name":"analytics:page_layout"})
        article_data["twitter_image_alt"] = get_content(soup, "meta",  {"name":"twitter:image:alt"})
        article_data["locale"] = get_content(soup, "meta",  {"property":"og:locale"})
        article_data["title"] = get_content(soup, "meta",  {"property":"og:title"})
        article_data["url"] = get_content(soup, "meta",  {"property":"og:url"})


    elif check_html_for_reuters_site_type(soup,s_type="article:section"):
        article_data["urls"] = get_all_hrefs_from_page(soup, add_root_page=root_page)
        article_data["r_site_type"] = "article:section"
    
    return article_data


if __name__ == "__main__":
    
    already_visited_sites = []
    known_article_sections = ["https://www.reuters.com/"]
    found_articles = []
    data = []

    found_articles.extend(known_article_sections)
    root_page = "https://www.reuters.com" # Remove last backslash

    i = 0
    article_idx = len(found_articles)
    
    #while i <= article_idx:
    while i <= 30:
        
        # Get url
        url = found_articles[i]
        
        print("sleeping..")
        
        time.sleep(SLEEPTIME)
        
        print(url)
        
        if url not in already_visited_sites:
            
            # get ready soup for analysis. If soup == None, because url is unavailabe, skip site.
            soup = get_ready_soup_html(url)
            
            if soup:
                hrefs = get_all_hrefs_from_page(soup, add_root_page=root_page)

                #Track site
                already_visited_sites.append(url)
                article_data = get_page_data(soup)
                
                # Check page type
                if article_data["r_site_type"] == "article:section":
                    
                    #Add urls to found articles, so you expand the data of website
                    for _url in article_data["urls"]:
                        
                        if _url not in found_articles:
                            found_articles.append(_url)
                            article_idx +=1
                            
                        if _url not in known_article_sections:
                            known_article_sections.append(_url)
                            
                elif article_data["r_site_type"] == "article":

                    data.append(article_data)
        
        i+=1




