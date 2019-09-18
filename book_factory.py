from dbconfig import db

from models import Book



def get_books_by_isbn(isbn):

    books_db_rows = _get_books_from_db('books.isbn', isbn)
    books = []

    _copy_books_from_db_object(books_db_rows, books)
    return books

def get_books_by_author(author):

    books_db_rows = _get_books_from_db('authors.name', author)
    books = []

    _copy_books_from_db_object(books_db_rows, books)
    return books

def get_books_by_title(title):

    books_db_rows = _get_books_from_db('books.title', title)
    books = []

    _copy_books_from_db_object(books_db_rows, books)
    return books
    
def _copy_books_from_db_object(src, dest):
    for book in src:
        temp_book = Book()
        temp_book.id, temp_book.isbn, temp_book.title, temp_book.author, temp_book.year, temp_book.rating = book
        # TODO: Change this to be done on the DB side
        if temp_book.rating:
            temp_book.rating = int(temp_book.rating)
        reviews = _get_book_reviews_from_db(book.id)
        for review in reviews:
            temp_book.reviews.append(review[0])
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
    return db.execute(f"SELECT review FROM reviews where book_id=:book_id", {'book_id':book_id})


search_func_table = {
    'isbn':get_books_by_isbn,
    'author':get_books_by_author,
    'title':get_books_by_title,
}



