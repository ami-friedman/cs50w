import os
import sys, traceback

from flask import Flask, session, render_template, request, redirect, url_for, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

try:
    from user_handler import UserHandler
except:
    print('working model')
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

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        userHandler = UserHandler(request.form.get('username'), request.form.get('password'))
        try:
            username = userHandler.login()
            if username:
                session['username']=username
                return redirect(url_for('index'))
            else:
                return redirect(url_for('login'))
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route("/logout", methods=["GET"])
def logout():
    # Clear the session
    session['username'] = None
    return redirect(url_for('login'))