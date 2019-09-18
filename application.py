import os
import sys, traceback

from flask import Flask, session, render_template, request, redirect, url_for, session, flash
from flask_session import Session

import errors


app = Flask(__name__)
print(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "blablaAmidjskdjh"
Session(app)

try:
    import user_factory
except Exception as e:
    print('Could not import: {e}')
finally:
    pass

try:
    from book_factory import search_func_table
except Exception as e:
    print(f'Could not import: {e}')
finally:
    pass

@app.context_processor
def inject_user():
    return dict(username=None)

@app.route("/")
def index():
    return render_template("index.html")

# Users
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        try:         
            user = user_factory.create(request.form.get('username'), request.form.get('password'))
            return redirect(url_for('search'))
        except errors.UserExists:
            flash('Username already taken')
            return redirect(url_for('register'))
        except Exception:
            traceback.print_exc(file=sys.stdout)
            return redirect(url_for('register'))
    else:
        return render_template('register.html')

@app.route("/login", methods=["POST"])
def login():
    try:
        user = user_factory.get(request.form.get('username'), request.form.get('password'))
        _store_user(user.id, user.username)
        return redirect(url_for('search'))
    except errors.InvalidPassword:
        flash('Wrong Password')
        return redirect(url_for('index'))
    except errors.UserDoesNotExist:
        flash('Wrong Username')
        return redirect(url_for('index'))
    except Exception:
        traceback.print_exc(file=sys.stdout)
        return redirect(url_for('index'))

@app.route("/logout", methods=["GET"])
def logout():
    _clear_user()
    return redirect(url_for('index'))

# Books
@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        books = search_func_table[request.form.get('topic')](request.form.get('search_term'))
        if len(books) == 0:
            flash('No matches found')
        _store_books(books)
        return redirect(url_for('results'))
    else:
        return render_template('search.html')


@app.route("/results", methods=["GET"])
def results():
    return render_template('results.html')


@app.route("/books/<isbn>", methods=["GET"])
def books(isbn):

    books = search_func_table['isbn'](isbn)
    return render_template('book.html', book = books[0])

@app.route("/review", methods=["POST"])
def review():
    add_review(session['id'],request.form.get('isbn'),request.form.get('review'),request.form.get('rating'))

    return redirect(url_for('results'))


def _store_books(books):
    session['books'] = books

def _store_user(id, username):
    session['id'] = id
    session['username'] = username

def _clear_user():
    session.pop('id', None)
    session.pop('username', None)



