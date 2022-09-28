import os
import sys

#Correct Woking folder
sys.path.append(os.path.abspath(os.path.join('.', 'src')))

from db.redis_dw import get_db, add_article_hashset, check_url_exist
import unittest


class Test_redis_db_instace(unittest.TestCase): 
           
    def test(self):
        try:
            get_db()
            
        except Exception as e:
            self.fail("get_db() raised {e} unexpectedly!". format(e=e))
        
        
if __name__ == '__main__':
    unittest.main()