from models import User
import errors
import traceback, sys

from dbconfig import db

def create(username, password):
    
    if _username_exist(username):
        raise errors.UserExists
    
    user = User(username,password)

    _insert_to_db(user)

    _set_id(user)
    return user

def get(username, password):
    if _username_exist(username):
        if _passwords_match(username, password):
            user = User()
            user.id, user.username, user.password = _get_from_db(username)
            return user
        else:
            raise errors.InvalidPassword
    else:
        raise errors.UserDoesNotExist
        
        
def _insert_to_db(user):
     try:
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", 
        {"username":user.username, "password":user.password})
        
        db.commit()

     except Exception as e:
         traceback.print_exc(file=sys.stdout)

def _get_from_db(username):
    return next(db.execute("SELECT id, username, password from users WHERE username=:username", {'username':username}))

def _username_exist(username):
    return db.execute("SELECT * from users WHERE username=:username", {'username':username}).rowcount > 0

def _passwords_match(username, password):
     p = next(db.execute("SELECT password from users WHERE username=:username", {'username':username}))[0]
     return p == password

def _set_id(user):
    user.id = next(db.execute("SELECT id from users WHERE username=:username", {'username':user.username}))[0]





