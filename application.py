import os
import sys, traceback

from flask import Flask, session, render_template, request, redirect, url_for, session, flash
from flask_session import Session


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
    from user_handler import UserHandler
except Exception as e:
    print('Could not import from user_handler: {e}')
finally:
    pass

try:
    from book_handler import func_table, add_review
except Exception as e:
    print(f'Could not import from book_handler: {e}')
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
        userHandler = UserHandler(request.form.get('username'), request.form.get('password'))
        try:
            userHandler.register()
            flash('Registration Complete')
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            flash('Registration Failed')
        finally:
            return redirect(url_for('index.html'))
    else:
        return render_template('register.html')

@app.route("/login", methods=["POST"])
def login():
    if request.method == 'POST':
        userHandler = UserHandler(request.form.get('username'), request.form.get('password'))
        try:
            user = userHandler.login()
            if user:
                session['username']=user.username
                session['id']=user.id
                return redirect(url_for('index'))
            else:
                flash("Username not found or password is incorrect")
                return redirect(url_for('index'))
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return redirect(url_for('index'))

@app.route("/logout", methods=["GET"])
def logout():
    # Clear the session
    session['username'] = None
    session['id'] = None
    return redirect(url_for('index'))

# Books
@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        topic = request.form.get('topic')
        search_term = request.form.get('search_term')
        print(topic, search_term)
        books = func_table[topic](search_term)
        if len(books) == 0:
            flash('No matches found')
        session['books'] = books
        return redirect(url_for('results'))
    else:
        if session['username']:
            return render_template('search.html')
        else:
            flash('Please Login')
            return redirect(url_for('index'))


@app.route("/results", methods=["GET"])
def results():
    return render_template('results.html')


@app.route("/books/<isbn>", methods=["GET"])
def books(isbn):

    books = func_table['isbn'](isbn)
    return render_template('book.html', book = books[0])

@app.route("/review", methods=["POST"])
def review():
    # add_review(session['id'],request.form.get('isbn'),request.form.get('review'),request.form.get('rating'))
    print(session['id'],request.form.get('isbn'),request.form.get('review'),request.form.get('rating'))

    return redirect(url_for('results'))



