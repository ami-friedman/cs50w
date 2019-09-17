from dbwrapper import db
import sys, traceback

class User():
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

    def create(self, username, password):
        self._username = username
        self._password = password
        if not self._is_username_exists():
            self._create()
        else:
            raise Exception('User already exists')
    
    def login(self):
        self._login()
        
    def _login(self):
        try:
            rows = db.execute("SELECT * from users WHERE username=:username", {'username':self._username})
            for user in rows:
                if user[2] == self._password:
                    self._id = user[0]
                    self._username = user[1]
                    self._password = user[2]
                print('user not found or passwords do not match')
        except Exception as e:
            traceback.print_exc(file=sys.stdout)

    def _create(self):
        try:
            db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", 
            {"username":self._username, "password":self._password})
            
            db.commit()

            rows = db.execute("SELECT id from users WHERE username=:username", {'username':self._username})
            self._id = next(rows)[0]

        except Exception as e:
            traceback.print_exc(file=sys.stdout)


    def _is_username_exists(self):
        if not self._username:
            raise Exception("Username not set")
        return db.execute("SELECT * from users WHERE username=:username", {'username':self._username}).rowcount > 0

    