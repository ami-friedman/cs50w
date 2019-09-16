from dbwrapper import db
import sys, traceback

class User():
    def __init__(self, username=None, password=None):
        self._username = username
        self._password = password

    def create(self, username, password):
        self._username = username
        self._password = password
        if not self._is_username_exists():
            self._create()
        else:
            raise Exception('User already exists')
    
    def login(self):
        return self._get_user()
        
    def _get_user(self):
        try:
            rows = db.execute("SELECT * from users WHERE username=:username", {'username':self._username})
            for user in rows:
                if user[2] == self._password:
                    return user[1]
                print('user not found or passwords do not match')
            return None
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return None

    def _create(self):
        try:
            db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", 
            {"username":self._username, "password":self._password})
            
            db.commit()
        except Exception as e:
            traceback.print_exc(file=sys.stdout)


    def _is_username_exists(self):
        if not self._username:
            raise Exception("Username not set")
        return db.execute("SELECT * from users WHERE username=:username", {'username':self._username}).rowcount > 0

    