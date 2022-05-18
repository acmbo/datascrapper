"""Analyzer for relationship inside data"""

import sys



from arc import Analyzer



class Relation_Analyzer(Analyzer):
    
    def __init__(self):
        self.db = get_db()
        