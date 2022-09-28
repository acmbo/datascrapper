from bs4 import BeautifulSoup
from bs4 import element 
from datetime import datetime
import re


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




def extract_article_data(article: dict, html:str):    
    """extracts data from html text of a dw article and adds it
    to the article meta data, stored in the dictionary which is given
    Args:
        article (dict): [description]
        url_source (str): [description]
        html (str): [description]
    Returns:
        [type]: [description]
    """
    
    soup = BeautifulSoup(html, "html.parser")
    
    # Get theme of website
    navpath = soup.find("div", {"id": "navPath"})
    
    if navpath:
        ahrefs = navpath.find_all("a")
        pagetheme = [theme.text.replace("\n", "") for theme in ahrefs]
        article['Themen'] = ";".join(pagetheme)
    
    h4article = soup.find("h4", {"class":"artikel"})  # Changed from article to artikel
    
    if h4article:
        article["h4article"]= h4article.text
    
    
    for li in soup.find_all("li"):
        
        if "Datum" in li.text:
            pattern: str = "[0-9]{2}.[0-9]{2}.[0-9]{4}"
            art_date: list = re.findall(pattern, li.text)
            
            if len(art_date)==1:
                article["Datum"] = art_date[0]
                
        if 'Themenseiten' in li.text:
            
            found_themes: list = []
            
            for a in li.findAll("a"):
                found_themes.append((a.text, a["href"]))
                
            article['Themenseiten'] = found_themes
        
        
        if 'Permalink' in li.text:
            
            for i, c in enumerate(li.contents):

                if "Permalink" in str(c):
                    try:
                        article['Permalink'] = li.contents[i+1].replace("\n","")
                    except:
                        print("No Autor found")
        
            
        if 'Schlagwörter' in li.text:
            
            found_key: list = []
            
            for a in li.findAll("a"):
                found_key.append(a.text)
                
            article['Schlagwörter'] = found_key
        
        
        if "Autorin" in li.text or "Autor" in li.text:

            for i, c in enumerate(li.contents):

                if "Autorin" in str(c) or "Autor" in str(c):
                    try:
                        article['Autorin/Autor'] = li.contents[i+1].replace("\n","")
                    except:
                        print("No Autor found")
    
    
    if article["title"] == "":
        title = soup.find("h1")
        if title:
            article["title"] = title.text
                        
    if article['abstract'] == "":
        intro = soup.find("p", {"class":"intro"}) 
        if intro:
            article['abstract'] = intro.text           
                        
                                  
    #DONT DELETE!!!!!
    
    # store text data
    #text = {'Text':'',
    #        'Title':'',
    #        'Article_Scene':''}
    
    # Right now text isnt needed for analysis!
    #    longtext = soup.find_all("div",{"class":"longText"})
    # article['Artikel'] = ' | '.join([get_article_text(txt) for txt in longtext])
            
    #for content in soup.find_all("div",{"id":"bodyContent"}):
        
    #    if content.find("h1"):
    #        
    #        text['Title'] = content.find("h1").text
    #        
    #    if content.find("h4"):
    #        
    #        text['Article_Scene'] = content.find("h4").text
    
    article["scrapedate"] = datetime.now().isoformat()
    
    url = article["url"]

    if len(url.split("/")) > 0:
        if "av" in url.split("/")[len(url.split("/"))-1]:
            article["video"]=True 
            
    return article
    
    

if __name__ == "__main__":
    
    import requests
    from mainpage import get_empty_article_meta_data
    

        
    base = "https://www.dw.com"
    url = '/de/ukraine-aktuell-ukrainer-spenden-ihrer-armee-präzise-satellitenfotos/a-62873667'
    
    html = requests.get(base+url).text
    
    article = get_empty_article_meta_data()
    
    extract_article_data(article, html)
