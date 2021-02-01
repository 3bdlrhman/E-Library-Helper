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
    
    def test_get_paginated_books(self):
        res = self.client().get('/books/')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data['books']))
       
    def test_404_sent_request_beyond_valid_page(self):
        res = self.client().get('/books/?page=11', json={'rating':1})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        
if __name__=='__main__':
    unittest.main()
        
