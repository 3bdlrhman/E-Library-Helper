from flaskr import create_app
from models import setup_db
import json
import unittest

class flaskr_testcase(unittest.TestCase):
    ''' this class represent the flaskr test case '''
    
    def setUp(self):
        """ define test variables and initialize app. """
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)
        
    def tearDown(self):
        ''' excuetes after each test even succes or failed '''
        pass
    
    def test_first_endpoint(self):
        """ Test first endPoint """
        res = self.client().get('/books')
        self.assertEqual(res.status_code, 200)
        
if __name__=='__main__':
    unittest.main()
        
