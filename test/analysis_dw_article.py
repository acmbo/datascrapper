"""Analysis error in article extraction"""

import os
import sys

#Correct Woking folder
sys.path.append(os.path.abspath(os.path.join('.', 'src')))


from utils.proxy import choose_proxy_from_proxyrotation
from dw.article import extract_article_data


url ="https://www.dw.com//de/zahlreiche-flugsaurier-in-atacama-wüste-entdeckt/a-61410235"  
# https://www.dw.com//de/ist-wasserstoff-der-energieträger-der-zukunft/a-61314634