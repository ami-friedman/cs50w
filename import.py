import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

class BookEntry:
    def __init__(self, isbn, title, author, year):
        self.isbn = isbn,
        self.author = author,
        self.title = title,
        self.year = year



def populate_authors(book_entries):
    for entry in book_entries:
        if db.execute("SELECT * FROM authors where name = :author", {'author':entry.author}).rowcount == 0:
            db.execute("INSERT INTO authors (name) VALUES (:author)", { 'author':entry.author })
            db.commit()

def populate_books(book_entries):
    for entry in book_entries:
        if db.execute("SELECT title FROM books WHERE title = :title", {'title': entry.title}).rowcount == 0:
            db.execute("INSERT INTO books (isbn, title, author_id, year) VALUES (:isbn, :title, (SELECT id FROM authors WHERE name = :name), :year)", { 'isbn':entry.isbn, 'title':entry.title, 'name': entry.author, 'year':entry.year})
            db.commit()


book_entries = []

with open('books.csv') as f:
    f_reader = csv.reader(f, delimiter=',')
    # Move passed the titles
    next(f_reader)
    for row in f_reader:
        entry = BookEntry(row[0], row[1], row[2], row[3] )
        book_entries.append(entry)
populate_authors(book_entries)
populate_books(book_entries)



