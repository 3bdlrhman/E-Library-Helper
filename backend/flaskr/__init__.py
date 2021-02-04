import os
from flask import Flask, request, abort, jsonify
import flask
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS
import random
from models import setup_db, Book

BOOKS_PER_SHELF = 8

def Paginate_books(request, all_books):
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * BOOKS_PER_SHELF
      end = start + BOOKS_PER_SHELF
      lst_of_books = [book.format() for book in all_books]
      books_to_show = lst_of_books[start:end]
      return books_to_show

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
  @app.route('/books/')
  def show_books():
    books = Book.query.all()
    books_list = Paginate_books(request, books)
    if len(books_list) == 0:
          return abort(404)
    else:
      return jsonify({
        'success': True,
        'books': books_list,
        'total_books': len(books)
      })

  # route that will update a single book's rating. 
  @app.route('/books/<int:book_id>', methods=['PATCH'])
  def change_book_rating(book_id):
    request_body = request.get_json()
    book = Book.query.get(book_id)
    if book is None:
      abort(404)
    if 'rating' in request_body:
      book.rating = int(request_body['rating'])
    
    try:
      book.update()
      return jsonify({
        'success': True,
        'id': book.id
      })
    except:
      return abort(422)
        
  # route that deletes specific book.       
  @app.route('/books/<book_id>', methods=['DELETE'])
  def delete_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
            abort(404)
  
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
    request_body = request.get_json()
    title= request_body.get('title', None)
    author= request_body.get('author', None)
    rating= request_body.get('rating', None)
    
    try:
      book = Book(title, author, int(rating))
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
  def Not_Found(error):
    return jsonify({
      'success': False,
      'message': 'resource not found',
      'status_code': 404
    }), 404
        
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'stauts_code': 422,
      'message': 'can not process the request'
    }), 422

  return app
