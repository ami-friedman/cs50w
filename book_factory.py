from dbconfig import db

from models import Book, Review

import errors

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
    
def _get_books(field, value):
    books_db_rows = _get_books_from_db(field, value)
    books = []
    _convert_db_object_to_books_array(books_db_rows, books)
    return books

def _convert_db_object_to_books_array(src, dest):
    for book in src:
        temp_book = Book()
        temp_book.id, temp_book.isbn, temp_book.title, temp_book.author, temp_book.year, temp_book.rating = book
        # TODO: Change this to be done on the DB side
        if temp_book.rating:
            temp_book.rating = int(temp_book.rating)
        else:
            temp_book.rating = 0
        reviews = _get_book_reviews_from_db(book.id)
        for review in reviews:
            temp_review = Review()
            temp_review.review, temp_review.rating, temp_review.user = review
            temp_book.reviews.append(temp_review)
            print(len(temp_book.reviews))
        dest.append(temp_book)

def _get_books_from_db(field, value):
    # Select all relevant fields
   return db.execute(f"SELECT books.id, books.isbn, books.title, authors.name, books.year, AVG(reviews.rating) as rating \
                       FROM books \
                       INNER JOIN authors on books.author_id = authors.id \
                       LEFT JOIN reviews on reviews.book_id=books.id \
                       WHERE {field} LIKE :value\
                       GROUP BY books.id, books.isbn, books.title, authors.name, books.year", 
                       {'value':'%' + value + '%'})

def _get_book_reviews_from_db(book_id):
    return db.execute(f"SELECT reviews.review, reviews.rating, users.username \
                        FROM reviews \
                        LEFT JOIN users on reviews.user_id = users.id \
                        WHERE book_id=:book_id", {'book_id':book_id})

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
}



