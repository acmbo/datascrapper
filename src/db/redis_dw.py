import redis
import pickle

REDISDB = 1

def preprocess_for_redis(article_dict):
    pickled_object = pickle.dumps(article_dict)
    return pickled_object


def preprocess_from_redis(db_value):
    return pickle.loads(db_value)


def get_db(db_number=REDISDB):
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
                    'Schlagw??rter': ['Russland',
                    'Belarus',
                    'Integration',
                    'Wirtschaft',
                    'Putin',
                    'Lukaschenko'],
                    'Artikel': {'Text': '\n Es gibt Ereignisse, die werden mit Spannung erwartet - und dann passiert lange nichts. So war das mit der Ann??herung zwischen Russland und Belarus. Seit drei Jahren dr??ngte Moskau auf eine engere Integration, um die schon seit den 1990er Jahren bestehenden Vertr??ge ??ber einen "Unionsstaat" umzusetzen. Der belarussische Machthaber Alexander Lukaschenko reiste immer wieder zum russischen Pr??sidenten Wladimir Putin, die beiden verhandelten oft stundenlang. Details wurden geheim gehalten.\xa0Eine Vereinbarung lie?? jedoch auf sich warten.\xa0 \n Das ??nderte sich erst vergangene Woche. Lukaschenko und Putin verk??ndeten am 10. September in Moskau, man habe sich auf 28 "Unionsprogramme" geeinigt,\xa0Fahrpl??ne, die die beiden L??nder noch enger aneinander binden sollen.\xa0Lukaschenko sprach von einem "Durchbruch", Putin beschrieb sie als "ernsten Schritt in Richtung der Schaffung eines gemeinsamen Wirtschaftsraums". Endg??ltig soll das Paket Anfang November beschlossen werden. \n <h2>Putin: zun??chst Wirtschaft, dann Politik</h2> \n Tritt nun das ein, wovor Oppositionelle in Belarus lange gewarnt und wogegen sie sogar protestiert hatten? Wird Russland Belarus wom??glich gar "schlucken"? Eine eindeutige Antwort scheint derzeit unm??glich. Von den Staatschefs auf beiden Seiten gab es zun??chst ??ffentlich\xa0Entwarnung. ??ber eine politische Integration habe man gar nicht gesprochen, so Putin. Gleichwohl deutete der russische Pr??sident an, eine "wirtschaftliche Grundlage" f??r eine sp??tere politische Integration legen zu wollen. \n Dabei sind Moskau und Minsk bereits Mitglieder in der Eurasischen Union, einem Prestige-Projekt Putins, mit dem der Kreml die wirtschaftliche Integration ehemaliger Sowjetrepubliken vorantreibt. Nun werden Russland und Belarus faktisch eine Vorreiterrolle ??bernehmen.\xa0\xa0\xa0 \n \n \xa0\xa0\xa0\xa0 \n <h2>Experte: Vage Formulierungen, wenig Konkretes\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0</h2> \n Was genau wurde vereinbart? Es geht unter anderem um gemeinsame Bankregeln, Kreditpolitik, Verbraucherschutz, Kampf gegen Geldw??sche, Verkehr, Landwirtschaft oder Tourismus. Ob und wann es eine gemeinsame W??hrung geben wird, ist noch unklar ist. Daf??r sei es zu fr??h, so Putin. \n Vieles sei sehr vage formuliert, sagt Lew Lwowskij, Wirtschaftsexperte beim belarussischen Forschungszentrum BEROC. "Das Problem sind die allgemein gehaltenen Formulierungen", so Lwowskij. Man habe sich lediglich "darauf geeinigt, sich k??nftig zu einigen". So tauche etwa 22 mal das Wort "Harmonisierung" in den Papieren\xa0auf, ohne dass konkret beschrieben werde, was das bedeuten soll.\xa0\xa0 \n \n Deutlich wurden dagegen Putin und Lukaschenko beim Thema Geld und Energie. Belarus bekommt bis 2022 russische Kredite in H??he von 630 Millionen US-Dollar. Die Summe ist Teil eines mehr als doppelt so gro??en Hilfspakets, das bereits zu einem fr??heren Zeitpunkt vereinbart worden war. Auch die Gaspreise sollen laut Vereinbarungen auf dem derzeitigen niedrigen Niveau bleiben, bevor 2023 ein gemeinsamer Gas- und ??lmarkt entsteht. Da die Gaspreise auf dem europ??ischen Markt derzeit in Rekordtempo steigen, d??rfte das das wirtschaftlich angeschlagene und immer st??rker von Russland abh??ngige Belarus besonders freuen. \n <h2>Integrationsank??ndigung vor Duma-Wahl</h2> \n Warum Lukaschenko ausgerechnet jetzt dem Integrationsfahrplan zustimmte, liegt auf der Hand. Seit der Machthaber in Minsk die\xa0Proteste der Opposition niederschlagen lie?? und der Westen darauf mit harten Sanktionen reagierte, ist Lukaschenko besonders von seinem engsten Verb??ndeten Russland abh??ngig. So d??rfte der Zeitpunkt der Ank??ndigung wohl nicht zuf??llig gew??hlt worden sein ??? einen Tag vor Beginn des gro?? angelegten russisch-belarussischen\xa0Milit??rman??vers "Zapad-2021"("Westen 2021") und eine Woche vor der Wahl der Staatsduma, der unteren Kammer des russischen Parlaments.\xa0\xa0 \n \n "F??r Putin ist es ??u??ert wichtig, seinen W??hlern ein Wahlgeschenk zu machen", sagt der Moskauer Politik-Experte Dmitrij Oreschkin. Russische W??hler m??gen "geopolitische Geschenke". Es soll der Eindruck entstehen, Russland w??rde Belarus "langsam ??bernehmen". Ob dies auch tats??chlich passiert, ist jedoch offen.\xa0\xa0\xa0 \n Die vereinbarten Ma??nahmen seien noch kein Ende belarussischer Souver??nit??t, sagen Experten in Minsk. "Doch gibt es einen Hinweis darauf, dass die beiden Seiten die Umsetzung der Vereinbarungen aus dem Jahr 1999 anstreben", sagt Andrej Kasakewitsch, Direktor des belarussischen Instituts "Politische Sph??re". In diesen gehe es um supranationale Organe und eine politische Vereinigung. Auch ein gemeinsames Parlament war fr??her im Gespr??ch, wurde aber jetzt offenbar ausgeklammert. \n Russland gehe es derzeit darum, "m??glichst viele institutionelle Mechanismen zu schaffen, mit denen es Einfluss auf Belarus aus??ben und es in seinem politischen und wirtschaftlichen Orbit halten kann." Das sei eine langfristige Strategie, die auch nach einem m??glichen Ende von Lukaschenkos Amtszeit weiter wirken soll, so Kasakewitsch.\n     \n',
                    'Title': 'Wird Russland Belarus schlucken?',
                    'Article_Scene': 'Die Redaktion empfiehlt'}}

    add_article(db, test_article)
    get_dw_article_by_url(db, '/de/wird-russland-belarus-schlucken/a-59181798')
    check_url_exist(db,'/de/wird-russland-belarus-schlucken/a-59181798')
