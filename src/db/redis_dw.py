import redis
import pickle

def preprocess_for_redis(article_dict):
    pickled_object = pickle.dumps(article_dict)
    return pickled_object


def preprocess_from_redis(db_value):
    return pickle.loads(db_value)


def get_db(db_number=0):
    db = redis.Redis(host='localhost', port=6379, db=db_number)
    return db


def add_article(db, article):
    db.set(article["url"], preprocess_for_redis(article))
    
    
    
def get_first_dw_articles(db):
    pass


def get_dw_article_by_url(db, url):
    return [preprocess_from_redis(db.get(url))]


def get_all_dw_article(db):
    return [keys for keys in db.scan_iter(match='*')]



def amount_of_articles_exist(db):
    return len([keys for keys in db.scan_iter(match='*')])


def check_url_exist(db, url):
    return len([keys for keys in db.scan_iter(match=bytes(url, 'utf-8'))])>0
   
 
def update_article(db,url,article):
    db.dw.update_one({'url': url}, 
                     {"$set": {"newfield": "abc"}}, 
                     upsert=False)



if __name__ == "__main__":

        
    db = get_db() 

    test_article = {'url': '/de/wird-russland-belarus-schlucken/a-59181798',
                    'title': '<h2>Wird Russland Belarus schlucken? </h2>',
                    'subtitle': '',
                    'abstract': 'Der Fahrplan zur engeren Integration zwischen Russland und Belarus klammert eine politische Vereinigung aus - vorerst. \xa0 ',
                    'image_title': '',
                    'mainarticle': False,
                    'video': False,
                    'meistgelesen': False,
                    'redaktionsempfehlung': False,
                    'Datum': '14.09.2021',
                    'Autorin/Autor': 'Roman Goncharenko, Sergey Satanovskiy, Arina Polsik',
                    'Permalink': 'https://p.dw.com/p/40Jt8',
                    'Themenseiten': [('Russland', '/de/russland/t-17284476'),
                    ('Wladimir Putin', '/de/wladimir-putin/t-17289915'),
                    ('Belarus', '/de/belarus/t-18456747')],
                    'Schlagwörter': ['Russland',
                    'Belarus',
                    'Integration',
                    'Wirtschaft',
                    'Putin',
                    'Lukaschenko'],
                    'Artikel': {'Text': '\n Es gibt Ereignisse, die werden mit Spannung erwartet - und dann passiert lange nichts. So war das mit der Annäherung zwischen Russland und Belarus. Seit drei Jahren drängte Moskau auf eine engere Integration, um die schon seit den 1990er Jahren bestehenden Verträge über einen "Unionsstaat" umzusetzen. Der belarussische Machthaber Alexander Lukaschenko reiste immer wieder zum russischen Präsidenten Wladimir Putin, die beiden verhandelten oft stundenlang. Details wurden geheim gehalten.\xa0Eine Vereinbarung ließ jedoch auf sich warten.\xa0 \n Das änderte sich erst vergangene Woche. Lukaschenko und Putin verkündeten am 10. September in Moskau, man habe sich auf 28 "Unionsprogramme" geeinigt,\xa0Fahrpläne, die die beiden Länder noch enger aneinander binden sollen.\xa0Lukaschenko sprach von einem "Durchbruch", Putin beschrieb sie als "ernsten Schritt in Richtung der Schaffung eines gemeinsamen Wirtschaftsraums". Endgültig soll das Paket Anfang November beschlossen werden. \n <h2>Putin: zunächst Wirtschaft, dann Politik</h2> \n Tritt nun das ein, wovor Oppositionelle in Belarus lange gewarnt und wogegen sie sogar protestiert hatten? Wird Russland Belarus womöglich gar "schlucken"? Eine eindeutige Antwort scheint derzeit unmöglich. Von den Staatschefs auf beiden Seiten gab es zunächst öffentlich\xa0Entwarnung. Über eine politische Integration habe man gar nicht gesprochen, so Putin. Gleichwohl deutete der russische Präsident an, eine "wirtschaftliche Grundlage" für eine spätere politische Integration legen zu wollen. \n Dabei sind Moskau und Minsk bereits Mitglieder in der Eurasischen Union, einem Prestige-Projekt Putins, mit dem der Kreml die wirtschaftliche Integration ehemaliger Sowjetrepubliken vorantreibt. Nun werden Russland und Belarus faktisch eine Vorreiterrolle übernehmen.\xa0\xa0\xa0 \n \n \xa0\xa0\xa0\xa0 \n <h2>Experte: Vage Formulierungen, wenig Konkretes\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0</h2> \n Was genau wurde vereinbart? Es geht unter anderem um gemeinsame Bankregeln, Kreditpolitik, Verbraucherschutz, Kampf gegen Geldwäsche, Verkehr, Landwirtschaft oder Tourismus. Ob und wann es eine gemeinsame Währung geben wird, ist noch unklar ist. Dafür sei es zu früh, so Putin. \n Vieles sei sehr vage formuliert, sagt Lew Lwowskij, Wirtschaftsexperte beim belarussischen Forschungszentrum BEROC. "Das Problem sind die allgemein gehaltenen Formulierungen", so Lwowskij. Man habe sich lediglich "darauf geeinigt, sich künftig zu einigen". So tauche etwa 22 mal das Wort "Harmonisierung" in den Papieren\xa0auf, ohne dass konkret beschrieben werde, was das bedeuten soll.\xa0\xa0 \n \n Deutlich wurden dagegen Putin und Lukaschenko beim Thema Geld und Energie. Belarus bekommt bis 2022 russische Kredite in Höhe von 630 Millionen US-Dollar. Die Summe ist Teil eines mehr als doppelt so großen Hilfspakets, das bereits zu einem früheren Zeitpunkt vereinbart worden war. Auch die Gaspreise sollen laut Vereinbarungen auf dem derzeitigen niedrigen Niveau bleiben, bevor 2023 ein gemeinsamer Gas- und Ölmarkt entsteht. Da die Gaspreise auf dem europäischen Markt derzeit in Rekordtempo steigen, dürfte das das wirtschaftlich angeschlagene und immer stärker von Russland abhängige Belarus besonders freuen. \n <h2>Integrationsankündigung vor Duma-Wahl</h2> \n Warum Lukaschenko ausgerechnet jetzt dem Integrationsfahrplan zustimmte, liegt auf der Hand. Seit der Machthaber in Minsk die\xa0Proteste der Opposition niederschlagen ließ und der Westen darauf mit harten Sanktionen reagierte, ist Lukaschenko besonders von seinem engsten Verbündeten Russland abhängig. So dürfte der Zeitpunkt der Ankündigung wohl nicht zufällig gewählt worden sein – einen Tag vor Beginn des groß angelegten russisch-belarussischen\xa0Militärmanövers "Zapad-2021"("Westen 2021") und eine Woche vor der Wahl der Staatsduma, der unteren Kammer des russischen Parlaments.\xa0\xa0 \n \n "Für Putin ist es äußert wichtig, seinen Wählern ein Wahlgeschenk zu machen", sagt der Moskauer Politik-Experte Dmitrij Oreschkin. Russische Wähler mögen "geopolitische Geschenke". Es soll der Eindruck entstehen, Russland würde Belarus "langsam übernehmen". Ob dies auch tatsächlich passiert, ist jedoch offen.\xa0\xa0\xa0 \n Die vereinbarten Maßnahmen seien noch kein Ende belarussischer Souveränität, sagen Experten in Minsk. "Doch gibt es einen Hinweis darauf, dass die beiden Seiten die Umsetzung der Vereinbarungen aus dem Jahr 1999 anstreben", sagt Andrej Kasakewitsch, Direktor des belarussischen Instituts "Politische Sphäre". In diesen gehe es um supranationale Organe und eine politische Vereinigung. Auch ein gemeinsames Parlament war früher im Gespräch, wurde aber jetzt offenbar ausgeklammert. \n Russland gehe es derzeit darum, "möglichst viele institutionelle Mechanismen zu schaffen, mit denen es Einfluss auf Belarus ausüben und es in seinem politischen und wirtschaftlichen Orbit halten kann." Das sei eine langfristige Strategie, die auch nach einem möglichen Ende von Lukaschenkos Amtszeit weiter wirken soll, so Kasakewitsch.\n     \n',
                    'Title': 'Wird Russland Belarus schlucken?',
                    'Article_Scene': 'Die Redaktion empfiehlt'}}

    add_article(db, test_article)
    get_dw_article_by_url(db, '/de/wird-russland-belarus-schlucken/a-59181798')
    check_url_exist(db,'/de/wird-russland-belarus-schlucken/a-59181798')
