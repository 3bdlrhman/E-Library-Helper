import os
from flask import Flask, request, abort, jsonify
import flask
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy #, or_
from flask_cors import CORS
import random
from models import setup_db, Book

BOOKS_PER_SHELF = 8

def Paginate_books(request, lst):
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * BOOKS_PER_SHELF
      end = start + BOOKS_PER_SHELF
      return lst[start:end]

# App Factory
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  # route that retrivies all books, paginated. 
  @app.route('/books')
  def show_books():
        books = Book.query.order_by(Book.id.asc()).all()
        lst_of_books = [book.format() for book in books]
        books_list = Paginate_books(request, lst_of_books)
        if len(books_list) == 0:
              return abort(404)
        else:
          return jsonify({
            'success': True,
            'books': books_list,
            'total_books': len(lst_of_books)
          })

  # route that will update a single book's rating. 
  @app.route('/books/<int:book_id>', methods=['PATCH'])
  def change_book_rating(book_id):
        book = Book.query.get(book_id)
        book.rating = int(request.get_json().get('rating', None))
        
        try:
          book.update()
          return jsonify({
            'success': True
          })
        
  # route that deletes specific book.       
  @app.route('/books/<book_id>', methods=['DELETE'])
  def delete_book(book_id):
        book = Book.query.get(book_id)
        
        try:
          book.delete()
          books_list = [b.format() for b in Book.query.all()]
          return jsonify({
            'success': True,
            'deleted': book_id,
            'books': books_list,
            'total_books': len(books_list)
          })
        except:
          return abort(404)

  # route that create a new book. 
  @app.route('/books', methods=['POST'])
  def create_book():
        title= request.get_json().get('title', None)
        author= request.get_json().get('author', None)
        rating= int(request.get_json().get('rating', None))
        
        try:
          book = Book(title, author, rating)
          book.insert()
          books = Book.query.order_by(Book.id).all()
          lst_of_books = [book.format() for book in books]
          books_list = Paginate_books(request, lst_of_books)
            
          return jsonify({
          'success': True,
          'created': book.id,
          'books': books_list,
          'total_books': len(lst_of_books)
        })
        except:          
          return abort(422)

  @app.errorhandler(404)
  def error_hapened(error):
        return jsonify({
          'success': False,
          'message': 'Error occurred',
          'status_code': 404
        }), 404

  return app