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
    def __init__(self, id=None, isbn=None, title=None, author=None, year=None, rating=0, gr_count=0, gr_rating=0):
        self._id = id
        self._isbn = isbn
        self._author = author
        self._title = title
        self._year = year
        self._reviews = []
        self._rating = rating
        self._gr_count = gr_count
        self._gr_rating = gr_rating
    
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
    
    @property
    def gr_rating(self):
        return self._gr_rating
    
    @property
    def gr_count(self):
        return self._gr_count
    
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
    
    @gr_rating.setter
    def gr_rating(self, gr_rating):
        self._gr_rating = gr_rating
    
    @gr_count.setter
    def gr_count(self, gr_count):
        self._gr_count = gr_count
    
    def to_dict(self):
        return {
            "title": self._title,
            "author": self._author,
            "year": self._year,
            "isbn": self._isbn,
            "review_count": self._gr_count,
            "average_score": self._gr_rating
        }

class Review:
     def __init__(self, id=None, review=None,rating=None, user=None):
        self._id = id
        self._review = review
        self._rating = rating
        self._user = user
    
     @property
     def id(self):
         return self._id
     
     @property
     def review(self):
         return self._review
     
     @property
     def rating(self):
         return self._rating
     
     @property
     def user(self):
         return self._user

     @id.setter
     def id(self, id):
         self._id = id

     @review.setter
     def review(self, review):
         self._review = review

     @rating.setter
     def rating(self, rating):
         self._rating = rating

     @user.setter
     def user(self, user):
         self._user = user 