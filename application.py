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
Session(app)

try:
    from user_handler import UserHandler
except Exception as e:
    print('Could not import from user_handler: {e}')
finally:
    pass

try:
    from book_handler import func_table
except Exception as e:
    print(f'Could not import from book_handler: {e}')
finally:
    pass

@app.context_processor
def inject_user():
    return dict(username=None)

@app.route("/")
def index():
    if 'username' in session:
        username=session['username']
        return render_template("index.html", username=username)
    return render_template("index.html")

@app.route("/test")
def test():
    print(request.form)


# Users
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        userHandler = UserHandler(request.form.get('username'), request.form.get('password'))
        try:
            userHandler.register()
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
        finally:
            return redirect(url_for('index'))
    else:
        return render_template('register.html')

@app.route("/login", methods=["POST"])
def login():
    if request.method == 'POST':
        userHandler = UserHandler(request.form.get('username'), request.form.get('password'))
        try:
            username = userHandler.login()
            if username:
                session['username']=username
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
    return redirect(url_for('index'))

@app.route("/results", methods=["GET"])
def results():
    # Clear the session
    return render_template('results.html')

@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        topic = request.form.get('topic')
        search_term = request.form.get('search_term')
        books = func_table[topic](search_term)
        session['books'] = books
        return redirect(url_for('results'))
    else:
        return render_template('search.html')

