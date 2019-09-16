from dbwrapper import db
import sys, traceback

class Book():
    def __init__(self, isbn, title, author, year, review=None):
        self._isbn = isbn
        self._author = author
        self._title = title
        self._year = year
        self._review = review
    
    @property
    def isbn(self):
        return self._isbn
    
    @property
    def title(self):
        return self._title
    
    @property
    def author(self):
        return self._author
   
    @property
    def year(self):
        return self._year
    
    @property
    def review(self):
        return self._review

class Books():

    _books = []

    def find_by_isbn(self, isbn):
        try:
            rows = db.execute("SELECT books.isbn, books.title, authors.name, books.year FROM books INNER JOIN authors on books .author_id = authors.id WHERE isbn LIKE :isbn", {'isbn':'%' + isbn + '%'})
            for book in rows:
               book_temp = Book(book[0],book[1], book[2], book[3])
               self._books.append(book_temp)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return None
    
    def find_by_title(self, title):
        try:
            rows = db.execute("SELECT books.isbn, books.title, authors.name, books.year FROM books INNER JOIN authors on books .author_id = authors.id WHERE title LIKE :title", {'title':'%' + title + '%'})
            for book in rows:
                book_temp = Book(book[0],book[1], book[2], book[3])
                self._books.append(book_temp)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return None
    
    def find_by_author(self, author):
        try:
            rows = db.execute("SELECT books.isbn, books.title, authors.name, books.year FROM books INNER JOIN authors on books .author_id = authors.id WHERE authors.name LIKE :author", {'author':'%' + author + '%'})
            for book in rows:
                book_temp = Book(book[0],book[1], book[2], book[3])
                self._books.append(book_temp)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return None

    @property
    def books(self):
        return self._books    



