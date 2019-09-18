from dbwrapper import db
import sys, traceback

class Book():
    def __init__(self, isbn, title, author, year, reviews=[], rating=None):
        self._isbn = isbn
        self._author = author
        self._title = title
        self._year = year
        self._reviews = reviews
        self._rating = rating
    
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
    def reviews(self):
        return self._reviews
   
    @property
    def rating(self):
        return self._rating
    
    @isbn.setter
    def isbn(self, isbn):
        self._isbn = isbn
   
    @title.setter
    def title(self, title):
        self._title = title
   
    @author.setter
    def author(self, author):
        self._author = author
    
    @year.setter
    def year(self, year):
        self._year = year
    
    @reiews.setter
    def reviews(self, reviews):
        self._reviews = reviews

    @rating.setter
    def rating(self, rating):
        self._rating = rating

class Books(object):

    def __init__(self):
        self._books = []
        super()

    def find_by_isbn(self, isbn):
        try:
            book_id = self._get_id_by_isbn(isbn)
            if db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {'book_id':book_id}).rowcount == 1:
                rows = db.execute("SELECT books.isbn, books.title, authors.name, books.year, reviews.review, reviews.rating FROM books INNER JOIN authors on books.author_id = authors.id INNER JOIN reviews on reviews.book_id=books.id WHERE isbn LIKE :isbn", {'isbn':'%' + isbn + '%'})
                for book in rows:
                    book_temp = Book(book[0],book[1], book[2], book[3], book[4], book[5])
                    self._books.append(book_temp)
            else:
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
    
    def add_review(self, review, rating, user_id, isbn):
        try:
             book_id = self._get_id_by_isbn(isbn)
             db.execute("INSERT INTO reviews (book_id, user_id, review, rating) VALUES (:book_id, :user_id, :review, :rating)", 
             {'book_id':book_id, 'user_id':user_id, 'review': review, 'rating':rating})
             db.commit()
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
    
    def _get_id_by_isbn(self, isbn):
        return next(db.execute("SELECT id FROM books WHERE isbn=:isbn", {'isbn':isbn}))[0]
    
    def _get_id_by_author(self, author):
        return next(db.execute("SELECT id FROM books WHERE author=:author", {'author':author}))[0]
    
    def _get_id_by_title(self, title):
        return next(db.execute("SELECT id FROM books WHERE title=:title", {'title':title}))[0]

    def _get_book_reviews(self, book_id):
        rows = db.execute("SELECT reviews FROM reviews WHERE book_id=:book_id", {'book_id':book_id})
        for row in rows:
            
             


    @property
    def books(self):
        return self._books    



