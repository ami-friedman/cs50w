class User:
    def __init__(self, username=None, password=None,id=None):
        self._username = username
        self._password = password
        self._id = id
    
    @property
    def username(self):
        return self._username
    
    @property
    def password(self):
        return self._password
    
    @property
    def id(self):
        return self._id

    @username.setter
    def username(self, u):
        self._username = u
    
    @password.setter
    def password(self, p):
        self._password = p
    
    @id.setter
    def id(self, id):
        self._id = id

class Book:
    def __init__(self, id=None, isbn=None, title=None, author=None, year=None, rating=None):
        self._id = id
        self._isbn = isbn
        self._author = author
        self._title = title
        self._year = year
        self._reviews = []
        self._rating = rating
    
    @property
    def id(self):
        return self._id
  
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
    
    @id.setter
    def id(self, id):
        self._id = id
    
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
    
    @reviews.setter
    def reviews(self, reviews):
        self._reviews = reviews

    @rating.setter
    def rating(self, rating):
        self._rating = rating

class Review:
     def __init__(self, id=None, review=None,rating=None):
        self._id = id
        self._review = review
        self._rating = rating