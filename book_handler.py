from book import Books


def find_book_by_isbn(isbn):
    books = Books()
    books.find_by_isbn(isbn)
    return books.books

def find_book_by_author(author):
    books = Books()
    books.find_by_author(author)
    return books.books

def find_book_by_title(title):
    books = Books()
    books.find_by_title(title)
    return books.books

def add_review(user_id, isbn, review, rating):
    books = Books()
    books.add_review(review, rating, user_id, isbn)




func_table = {
        'isbn':find_book_by_isbn,
        'title': find_book_by_title,
        'author': find_book_by_author
    }