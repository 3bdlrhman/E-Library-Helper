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
        
    def test_update_book_rating(self):
        res = self.client().patch('/books/16', json={'rating': 5})
        data = json.loads(res.data)
        book = Book.query.filter(Book.id==26).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['rating'], 5)
        
    def test_get_book_search_with(self):
        res = self.client().post('/books', json={'search':'Great'})
        data = json.loads(res.data)
        self.assertEqual(len(data['books']), 1)

    def test_get_book_search_without(self):
        res = self.client().post('/books', json={'search':'hipopo'})
        data = json.loads(res.data)
        self.assertTrue(data['not_exist'])
        
if __name__=='__main__':
    unittest.main()
        
