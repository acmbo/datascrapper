"""utility class and functions for data analysis"""
import sys
from pathlib import Path
from datetime import datetime

import networkx as nx

# For dev purposes, so you can find db.redis
path = Path(__file__)
if path.parent.name == 'analyzer':
    sys.path.append(str(path.parents[1]))
    
    
import numpy as np
import pandas as pd
import requests
from db.redis_dw import get_db, get_all_dw_article, get_dw_article_by_url
from db.redis_dw import *

def get_redis_data(db):
    """Generator for returning data from redis db"""
    keys = np.array(get_all_dw_article(db))
    for key in keys:
        #print("KEY: ", key)
        yield get_dw_article_by_url(db, key, hset=True)


class Analyzer:
    """Analyzer Meta Class
    """
    def __init__(self, dbnumber):
        self.used_db = dbnumber
        self.date_today = datetime.today()
        
    
    def connect_to_db(self):
        db = get_db()
        return db
    
    
    def get_all_keys_with_date(self):
        redis_data =   [] # np.array([])
        # Faster to append to list first and convert to numpy array, https://stackoverflow.com/questions/29839350/numpy-append-vs-python-append
        
        with self.connect_to_db() as db:
            for data in get_redis_data(db):
                try: 
                    key=data["url"]
                    val=data["Datum"]
                except:
                    #print("Error on ", data)
                    key = None
                    val = None
                redis_data.append((key, val))
                
        return np.array(redis_data)
    
    
    def get_data_filtered_by_time(self, daydelta: int = None):
        """Get Keys from Redis DB filtered by a time delta. None as daydelta is possible, so you get all keys from db

        Args:
            daydelta (int, optional): Timedelta in days. Defaults to None.

        Returns:
            valid_keys (array): array of tuples of correct keys from db
        """
        
        rd = self.get_all_keys_with_date()

        valid_keys = []
        
        for d in rd:
            if isinstance(d[1], str) and d[1] != "":    # Clean Data for invalid entrys
                #print("KEY: ", d[1])
                datetime_object = datetime.strptime(d[1], '%d.%m.%Y')
                #print(datetime_object)
                timedelta = datetime.today() - datetime_object
                
                if daydelta and timedelta.days < daydelta:
                    valid_keys.append((d[0], datetime_object))
                    
                elif daydelta == None:
                    valid_keys.append((d[0], datetime_object))
                    
        return np.array(valid_keys)    
    
    
    def get_graph_Data_by_time(self, daydelta: int = None, get_themes: bool =False):
        """Get Graph of Keywords used in articles from Redis DB filtered by a time delta. None as daydelta is possible, so you get all keys from db

        Args:
            daydelta (int, optional): Timedelta in days. Defaults to None.

        Returns:
            networkx.graph: Graph of Keywords, connected by mentionings in articles
        """
        data = self.get_data_filtered_by_time(daydelta=daydelta)
    
        G = nx.Graph()
        
        with self.connect_to_db() as db:
            
            for entry in data:
                d = get_dw_article_by_url(db, entry[0], hset=True)
                keywords = d["Schlagwörter"]
                
                if get_themes:
                    themes = d["Themenseiten"]
                    themes = [th.split(",")[0].replace("'","").replace("(","") for th in themes]

                for keyword_a in keywords:
                    for keyword_b in keywords:
                        if keyword_a != keyword_b:                            
                            if (keyword_a, keyword_b) in G.edges:
                                G.edges[keyword_a, keyword_b]["weight"] += 1
                            else:
                                if get_themes:
                                    G.add_edge(keyword_a, keyword_b, weight=1, themes=themes)
                                else:
                                    G.add_edge(keyword_a, keyword_b, weight=1)
        return G    
    
    
    def get_keywords_by_time(self, daydelta: int = None):
        """Get Graph of Keywords used in articles from Redis DB filtered by a time delta. None as daydelta is possible, so you get all keys from db

        Args:
            daydelta (int, optional): Timedelta in days. Defaults to None.

        Returns:
            networkx.graph: Graph of Keywords, connected by mentionings in articles
        """
        data = self.get_data_filtered_by_time(daydelta=daydelta)
    
        G = nx.Graph()
        
        with self.connect_to_db() as db:
            
            all_keywords = []
            
            for entry in data:
                d = get_dw_article_by_url(db, entry[0], hset=True)
                keywords = d["Schlagwörter"]
                
                all_keywords.append(keywords)


        return all_keywords
    
    
    def get_keyword_amount(self,top=0, daydelta: int = None):
        # Get Keywords Table with amount of use

        key = self.get_keywords_by_time(daydelta=daydelta)
        
        #Flatten keywordlist
        flattened_keys = []
        for sublist in key:
            flattened_keys.extend(sublist)
            
        key_data = {}
        for word in flattened_keys:
            if word not in key_data.keys():
                key_data[word]=1
            else:
                key_data[word]+=1

  
        df = pd.DataFrame(key_data, index=[0]).transpose()
        
        df.columns = ["Amount"]
        df.sort_values("Amount", ascending=False, inplace=True)
        
        if top>0:
            df = df.head(top)

        return_data = {}
        
        for ind, val in zip(df.index, df["Amount"].values):
            return_data[ind]= int(val)    

        return return_data
    
    
    def get_keyword_raw(self, daydelta:int = None):
            # Get Keywords Table with amount of use

        key = self.get_keywords_by_time(daydelta)
        
        #Flatten keywordlist
        flattened_keys = []
        for sublist in key:
            flattened_keys.extend(sublist)
        
        flattened_keys = [word.replace(" ", "-") for word in flattened_keys]
        
        return flattened_keys
    
    
    def send_kw_monht_data_to_api(self, data, internal=True):
        if internal:
            url="http://127.0.0.1:5000/meta/keywordsmonth/"
        else:
            url="https://stephanscorner.de/meta/keywordsmonth/"
        r = requests.post(url, json=data)
        return r


    def send_kw_week_data_to_api(self, data, internal=True):
        if internal:
            url="http://127.0.0.1:5000/meta/keywordsweek/"
        else:
            url="https://stephanscorner.de/meta/keywordsweek/"
        r = requests.post(url, json=data)
        return r
    
    
    def send_delete_req_month(self, internal=True):
        if internal:
            url="http://127.0.0.1:5000/meta/keywordsmonth/"
        else:
            url="https://stephanscorner.de/meta/keywordsmonth/"
        r = requests.delete(url)
        return r

    def send_delete_req_week(self, internal=True):
        if internal:
            url="http://127.0.0.1:5000/meta/keywordsweek/"
        else:
            url="https://stephanscorner.de/meta/keywordsweek/"
        r = requests.delete(url)
        return r
    
    
    def send_raw_to_api_month(self, raw_data, internal=True):
        """post objects data to server api. Internal argument used for determining if you post to a internalt test server or to productive online server

        Args:
            internal (bool, optional): Send data to internal test server or online productive system. Defaults to True, which sends data to internal test server.
        """
        post_data = {
            'keywords': (None, " ".join(raw_data)),
        }

        if internal:
            url="http://127.0.0.1:5000/themegraph/keywordsrawmonth/"
        else:
            url="https://stephanscorner.de/themegraph/keywordsrawmonth/"

        response = requests.post(url, files=post_data)
        return response


    def send_raw_to_api_week(self, raw_data, internal=True):
        """post objects data to server api. Internal argument used for determining if you post to a internalt test server or to productive online server

        Args:
            internal (bool, optional): Send data to internal test server or online productive system. Defaults to True, which sends data to internal test server.
        """
        post_data = {
            'keywords': (None, " ".join(raw_data)),
        }

        if internal:
            url="http://127.0.0.1:5000/themegraph/keywordsrawweek/"
        else:
            url="https://stephanscorner.de/themegraph/keywordsrawweek/"

        response = requests.post(url, files=post_data)
        return response


    def send_delete_req_raw_month(self, internal=True):
        if internal:
            url="http://127.0.0.1:5000/themegraph/keywordsrawmonth/"
        else:
            url="https://stephanscorner.de/themegraph/keywordsrawmonth/"

        r = requests.delete(url)
        return r
    

    def send_delete_req_raw_week(self, internal=True):
        if internal:
            url="http://127.0.0.1:5000/themegraph/keywordsrawweek/"
        else:
            url="https://stephanscorner.de/themegraph/keywordsrawweek/"

        r = requests.delete(url)
        return r
    
    
    
    
    def send_postings_to_api(self, data, endpoint: str = "postingsweek/", internal=True):
        """post objects data to server api. Internal argument used for determining if you post to a internalt test server or to productive online server

        Args:
            internal (bool, optional): Send data to internal test server or online productive system. Defaults to True, which sends data to internal test server.
        """
        posts ={
            "posts":[],
            "dates":[]
        }
        
        if endpoint not in ["postingsweek/","postingsmonth/", "postingsyear/"]:
            return "Wrong Endpoints" 
        
        for url, date in data:
            if date not in posts["dates"]:
                posts["posts"].append(1)
                posts["dates"].append(date)
            else:
                posts["posts"][posts["dates"].index(date)] +=1
        
        responses=[]
           
        for i in range(len(posts["dates"])):
        
            post_data = {
                'post': (None, posts["posts"][i]),
                'date': (None, posts["dates"][i].isoformat()),
            }
            
            if internal:
                url="http://127.0.0.1:5000/meta/"+ endpoint
            else:
                url="https://stephanscorner.de/meta/" + endpoint

            response = requests.post(url, files=post_data)
            
            responses.append(response.status_code)
            
        return responses
    
    
    
    def send_delete_to_postings(self, endpoint: str = "postingsweek/", internal=True):
        
        if endpoint not in ["postingsweek/","postingsmonth/", "postingsyear/"]:
            return "Wrong Endpoints" 
        
        if internal:
            url="http://127.0.0.1:5000/meta/"+ endpoint
        else:
            url="https://stephanscorner.de/meta/" + endpoint
        r = requests.delete(url)
        return r
    
    
    def send_graph_to_api(self, endpoint: str = "themeGraphDaily/", internal=True, daydelta:int = None):
                
    
        if endpoint not in ["themeGraphWeekly/","themeGraphMonthly/", "themeGraphDaily/"]:
            return "Wrong Endpoints" 

        if not daydelta:
            if endpoint == "themeGraphDaily/":
                daydelta = 1
            elif endpoint == "themeGraphWeekly/":
                daydelta = 7
            elif endpoint == "themeGraphMonthly/":
                daydelta = 30
        
        G = self.get_graph_Data_by_time(daydelta=daydelta)

        data = {"nodes":[],
                "links":[]}
        for entry in list(G.edges):
            source, target = entry
            data_entry={
                "source": source,
                "target": target,
                "value": 1,
                "urls":""
            }
            data["links"].append(data_entry)
        
        
        # Min Max normalization
        max_val = 0
        min_val = 1
        sum_vals = 0

        
        for entry in list(G.degree()):
            data_entry = {"id": entry[0], "group": "1", "value": entry[1]} 
            
            if entry[1] > max_val:
                max_val = entry[1]
                
            sum_vals += entry[1]
                
            data["nodes"].append(data_entry)

        
        for entry in data["nodes"]:
            entry["value"] = round(min_val + ((entry["value"]  * (max_val -min_val))/ sum_vals),3) 

        

        if internal:
            url="http://127.0.0.1:5000/themegraph/" + endpoint
        else:
            url="https://stephanscorner.de/themegraph/" + endpoint
            
        r = requests.post(url, json=data)
        return r
    
    
    
    
    
    def main(self):
        # Create data for website
        
        # Graph data
        #G = self.get_graph_Data_by_time(daydelta=120)
        #data = self.get_data_filtered_by_time(daydelta=120)
        
        # Get Keywords for api
        keyW_data_week = self.get_keyword_amount(daydelta=7, top=20)  #Weekly
        keyW_data_month = self.get_keyword_amount(daydelta=30, top=20)  #Monthly
        
        # Get raw Keywords for api
        key_raw_week = self.get_keyword_raw(daydelta=7)
        key_raw_month = self.get_keyword_raw(daydelta=30)
        
        
        # Get Postings
        data_7 = self.get_data_filtered_by_time(daydelta=7)
        data_month = self.get_data_filtered_by_time(daydelta=30)
        data_complete = self.get_data_filtered_by_time()
        
        
        responses = {}  
        
        # Postings Data
        responses["Clean Postings Week"] = self.send_delete_to_postings(endpoint = "postingsweek/", internal=False)
        responses["Post Postings Week"] = self.send_postings_to_api(data_7, endpoint="postingsweek/", internal=False) 

        responses["Clean Postings Month"] = self.send_delete_to_postings(endpoint = "postingsmonth/", internal=False)
        responses["Post Postings Month"] = self.send_postings_to_api(data_month, endpoint="postingsmonth/", internal=False) 
        
        responses["Clean Postings Year"] = self.send_delete_to_postings(endpoint = "postingsyear/", internal=False)
        responses["Post Postings Year"] = self.send_postings_to_api(data_complete, endpoint="postingsyear/", internal=False) 

        
        # Clean api db
        ## Raw data
        responses["Clean Month Raw Data"]= self.send_delete_req_raw_month(internal=False)
        responses["Clean Weekly Raw Data"] = self.send_delete_req_raw_week(internal=False)

        ## Keywordtables
        responses["Clean Month tables Data"] = self.send_delete_req_month(internal=False)
        responses["Clean Weekly tables Data"] = self.send_delete_req_week(internal=False)
        
        # Send new data to api
        ## Raw data
        responses["Post Raw KW Week"] = self.send_raw_to_api_week(key_raw_week, internal=False)
        responses["Post Raw KW Month"] = self.send_raw_to_api_month(key_raw_month, internal=False)
        
        ## Keywordtables
        responses["Post KW tables Week"] = self.send_kw_week_data_to_api(keyW_data_week,  internal=False)
        responses["Post KW tables Month"] = self.send_kw_monht_data_to_api(keyW_data_month, internal=False)
        
        responses["Post Graph Daily"]  = self.send_graph_to_api(endpoint="themeGraphDaily/", internal=False)
        responses["Post Graph Monthly"]  = self.send_graph_to_api(endpoint="themeGraphMonthly/", internal=False)
        responses["Post Graph Weekly"]  = self.send_graph_to_api(endpoint="themeGraphWeekly/", internal=False)

        
        
        return responses

if __name__ =="__main__":
    
    an = Analyzer(1)
    #an.send_graph_to_api(daydelta=150)

    """
    G = an.get_graph_Data_by_time(daydelta=120)
    data = an.get_data_filtered_by_time(daydelta=120)
    key_data = an.get_keyword_amount(top=20)
    key_raw = an.get_keyword_raw(daydelta=120)
    r1 = an.send_delete_req_month()
    r = an.send_kw_monht_data_to_api(key_data)
    r2 = an.send_raw_to_api_month(key_raw)
        #"themeGraphWeekly/","themeGraphMonthly/", "themeGraphDaily/"]
    r1 = an.send_graph_to_api(endpoint="themeGraphDaily/", internal=True, daydelta = 150)
    r2 = an.send_graph_to_api(endpoint="themeGraphMonthly/", internal=True, daydelta = 150)
    r3 = an.send_graph_to_api(endpoint="themeGraphWeekly/", internal=True, daydelta = 150)
    # Get Postings
    data_7 = an.get_data_filtered_by_time(daydelta=7)
    data_month = an.get_data_filtered_by_time(daydelta=30)
    data_complete = an.get_data_filtered_by_time()
    
    
    responses = {}  
    
    # Postings Data
    responses["Clean Postings Week"] = an.send_delete_to_postings(endpoint = "postingsweek/", internal=True)
    responses["Post Postings Week"] = an.send_postings_to_api(data_7, endpoint="postingsweek/", internal=True) 

    responses["Clean Postings Month"] = an.send_delete_to_postings(endpoint = "postingsmonth/", internal=True)
    responses["Post Postings Month"] = an.send_postings_to_api(data_month, endpoint="postingsmonth/", internal=True) 
    
    responses["Clean Postings Year"] = an.send_delete_to_postings(endpoint = "postingsyear/", internal=True)
    responses["Post Postings Year"] = an.send_postings_to_api(data_complete, endpoint="postingsyear/", internal=True) 
    
    rep = an.main()
    print(rep)

    """
    

    
    
    
    # Not used:
    """
    import plotly.graph_objs as go
    from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
    import plotly
    import plotly.io as pio
    pio.renderers.default = "vscode"

    pos = nx.spring_layout(G, seed=1969, weight='weight')

    for n, p in pos.items():
        G.nodes[n]['pos'] = p

    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5,color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='RdBu',
        reversescale=True,
        color=[],
        size=15,
        colorbar=dict(
            thickness=10,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)))

    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
    print("here")
    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color']+=tuple([len(adjacencies[1])])
        node_info = adjacencies[0] +' # of connections: '+str(len(adjacencies[1]))
        node_trace['text']+=tuple([node_info])
    print("here")
    fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='<br>AT&T network connections',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="No. of connections",
                        showarrow=False,
                        xref="paper", yref="paper") ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    print("here")
    iplot(fig)
    plotly.plot(fig)



    import spacy
    sp_sm = spacy.load('de_core_news_sm')
    sp_em = spacy.load('de_dep_news_trf')

    import unicodedata
    
    
    with an.connect_to_db() as db:
        article = get_dw_article_by_url(db, data[5][0], hset=True)
        
    print(article)

    text = unicodedata.normalize("NFKD",article["Artikel"]["Text"])
    text = text.replace("</h2>", "").replace("<h2>", "").replace("\n", "")
    
    def spacy_ner_get_LOC(document,spacy_model):
        return {(ent.text.strip(), ent.label_) for ent in spacy_model(document).ents if ent.label_ in ['LOC', 'GPE'] }
    
    def spacy_ner(document, spacy_model):
        return {(ent.text.strip(), ent.label_) for ent in spacy_model(document).ents}

    
    
    
    sp_em = spacy.load('de_dep_news_trf')
    
    with open("test_article_txt.txt","r") as f:
        test_ar = f.readline()
    
    x = spacy_ner(test_ar, sp_em)
    x = spacy_ner_get_LOC(test_ar, sp_sm)
    """
    
