from bs4 import BeautifulSoup
from bs4 import element 
from datetime import datetime
import dateutil
import json
import unicodedata
from dw.mainpage import find_term_in_bstag_attr, partialfind_term_in_bstag_attr
from utils.textrank import TextRank4Keyword


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
    meta = soup.find_all("meta")
    scripts = soup.find_all("script")
    article_text = soup.find_all("article")
    content = []
        
    # Get theme of website
    #  <div class="sc-eWhHU sc-dyTUbJ hlxmwH dumiuG sc-llCxYp gpBzkq kicker sc-fpOQxu cmdPrs" data-tracking-name="content-detail-kicker"><span>Musik</span><span><a class="sc-fFGjHI hpwUFy" tabindex="0" href="/de/deutschland/s-12321">Deutschland</a></span></div>
    navpath = soup.find("div", {"data-tracking-name": "content-detail-kicker"})
    
    if navpath:
        ahrefs = navpath.find_all("span")
        pagetheme = [theme.text.replace("\n", "") for theme in ahrefs]
        
        if len(pagetheme) > 0:
            article['Themen'] = ";".join(pagetheme)
            article['Themenseiten'] = pagetheme[0]
    
    h4article = soup.find("h4", {"class":"artikel"})  # Changed from article to artikel
    
    if h4article:
        article["h4article"]= h4article.text
        
    for entry in partialfind_term_in_bstag_attr(meta,'property','og:url'):
        article['Permalink'] =  entry["content"]
    
    for entry in partialfind_term_in_bstag_attr(meta,'property','og:description'):
        article['abstract'] =  entry["content"]    
    

    #<script data-rh="true" type="application/ld+json">{"@context":"https://schema.org","@type":"NewsArticle","mainEntityOfPage":{"@type":"WebPage","@id":"https://www.dw.com/de/u21-moukoko-nach-rassistischen-beleidigungen-schockiert/a-66010071"},"publisher":{"@type":"Organization","name":"Deutsche Welle","logo":{"@type":"ImageObject","url":"https://dw.com/images/icons/favicon-180x180.png","width":"180","height":"180"}},"author":[{"@type":"Organization","name":"Deutsche Welle","url":"https://www.dw.com"}],"headline":"U21: Moukoko nach rassistischen Beleidigungen schockiert","image":["https://static.dw.com/image/66010031_804.jpg","https://static.dw.com/image/66010031_604.jpg"],"datePublished":"2023-06-23T08:01:19.096Z","dateModified":"2023-06-23T15:39:29.609Z"}</script>
    for entry in partialfind_term_in_bstag_attr(scripts,'type','application/ld+json'):
        res = json.loads(entry.string)
        if "uploadDate" in res.keys():
            article["Datum"] = dateutil.parser.isoparse(res["uploadDate"]).strftime("%Y-%m-%d")
        if "datePublished" in res.keys():
            article["Datum"] = dateutil.parser.isoparse(res["datePublished"]).strftime("%Y-%m-%d")
        if "author" in res.keys():
            article['Autorin/Autor'] = [aut["name"] for aut in res["author"]]
        


    title = soup.find("h1")
    if title:
        article["title"] = title.text
        content.append(title.text)
                        

    for entry in article_text:
        for p in entry.find_all("p",text=True):
            content.append(unicodedata.normalize("NFKD", p.text).replace("nob/uh (dpa, afp)",""))           
    
    if len(content) > 0:      
        articletxt = ". ".join(content)                      
        rank = TextRank4Keyword()
        rank.analyze(articletxt, 
                        candidate_pos=['NOUN', 'PROPN'], 
                        window_size=4, lower=False, stopwords=list())

        keywords=rank.get_keywords(number=8)
        article['Schlagwörter'] = keywords   
  
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
