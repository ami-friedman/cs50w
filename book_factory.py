import requests

from dbconfig import db

from models import Book, Review

import errors

# APIs
def get_book_by_isbn(isbn):
    rows = _get_books_from_db('books.isbn', isbn, False)
    if rows.rowcount > 0:
        book = Book()
        _populate_book_data(book, next(rows))
        _populate_book_reviews(book)
        return book
    return None

def get_books_by_isbn(isbn):
    return _get_books('books.isbn', isbn)

def get_books_by_author(author):
    return _get_books('authors.name', author)

def get_books_by_title(title):
    return _get_books('books.title', title)

def add_review(user_id, book_id, review, rating):
    if _num_reviews_exceeded(user_id, book_id):
        raise errors.NumReviewsExceeded
    _add_review(user_id, book_id, review, rating)

# Utility Helpers  
def _get_books(field, value):
    books_db_rows = _get_books_from_db(field, value, True)
    if books_db_rows.rowcount > 0:
        books = []
        _create_books_array_from_db_object(books_db_rows, books)
        return books
    return None

def _populate_book_data(book, row):
    book.id, book.isbn, book.title, book.author, book.year, book.rating = row
    if book.rating:
        book.rating = int(book.rating)
    else:
        book.rating = 0

def _populate_book_reviews(book):
    reviews = _get_book_reviews_from_db(book.id)
    for review in reviews:
            temp_review = Review()
            temp_review.review, temp_review.rating, temp_review.user = review
            book.reviews.append(temp_review)
    book.gr_count, book.gr_rating = _get_gr_review(book.isbn)
    book.gr_rating = int(float(book.gr_rating))

def _create_books_array_from_db_object(rows, books):
    for row in rows:
        book = Book()
        _populate_book_data(book, row)
        # _populate_book_reviews(book)
        books.append(book)

def _get_books_from_db(field, value, pattern_match):
    operation = 'LIKE' if pattern_match else '='
    return db.execute(f"SELECT books.id, books.isbn, books.title, authors.name, books.year, AVG(reviews.rating) as rating \
                       FROM books \
                       INNER JOIN authors on books.author_id = authors.id \
                       LEFT JOIN reviews on reviews.book_id=books.id \
                       WHERE {field} {operation} :value\
                       GROUP BY books.id, books.isbn, books.title, authors.name, books.year", 
                       {'value':'%' + value + '%'})

def _get_book_reviews_from_db(book_id):
    return db.execute(f"SELECT reviews.review, reviews.rating, users.username \
                        FROM reviews \
                        LEFT JOIN users on reviews.user_id = users.id \
                        WHERE book_id=:book_id", {'book_id':book_id})

def _get_gr_review(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "MF4Rh26XdghAaxuBOYQojA", "isbns": isbn}).json()
    return res['books'][0]['work_reviews_count'], res['books'][0]['average_rating']

def _num_reviews_exceeded(user_id, book_id):
    return db.execute("SELECT * from reviews where book_id=:book_id and user_id=:user_id", {'book_id':book_id, 'user_id':user_id}).rowcount > 0

def _add_review(user_id, book_id, review, rating):
    db.execute("INSERT INTO reviews (book_id, user_id, review, rating) VALUES (:book_id, :user_id, :review, :rating)", 
              {'book_id':book_id, 'user_id':user_id, 'review': review, 'rating':rating})
    db.commit()

search_func_table = {
    'isbn':get_books_by_isbn,
    'author':get_books_by_author,
    'title':get_books_by_title,
    'add_review':add_review,
    'single':get_book_by_isbn,
}



