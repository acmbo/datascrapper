"""Analyzer for geolocation of data"""

from arc import Analyzer
import spacy

nlp = spacy.load("de_core_news_md")



data = an.get_data_filtered_by_time(daydelta=7)



with an.connect_to_db() as db:

    d = get_dw_article_by_url(db, data[2][0], hset=True)


st = ", ".join(d["Schlagwörter"])
doc = nlp(st)
for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)


st = d["abstract"]
doc = nlp(st)
for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)

for s in d["Schlagwörter"]:
    location = geocoder.geocode(s, language="de")  #    ({"country":s}, language="de")
    print(f"Wort: {s}, loc: {location}")




city=<city>
county=<county>
state=<state>
country=<country>
 
class Geo_Analyzer(Analyzer):
    
    def __init__(self):
        from geopy.geocoders import OpenCage
        geocoder = OpenCage("0b5d88bb887e4e09a4490b972e4f8191", user_agent="DW_Scrapper")
        location = geocoder.geocode("175 5th Avenue NYC")
        
        from geopy.geocoders import OpenMapQuest
        geocoder = OpenMapQuest("7SSzwmuevGvKraUB5A8WIfLHXt6xxyfD", user_agent="DW_Scrapper")
        location = geocoder.geocode("175 5th Avenue NYC")
        