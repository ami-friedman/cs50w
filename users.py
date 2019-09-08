from application import db

class User():
    def __init__(self, id=None):
        self._username = None
        self._password = None

    def create(self, username, password):
        self._username = username
        self._password = password
        # Check of username taken, if yes, throw already exists exception
        if not self._is_username_exists():
            self._create()
        else:
            raise 'User already exists'
    
    def _create(self):
        try:
            db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", 
            {"username":self._username, "password":self._password})
            
            db.commit()
        except Exception as e:
            print(e)


    def _is_username_exists(self):
        if not self._username:
            raise Exception("Username not set")
        return db.execute("SELECT * from users WHERE username=:username", {'username':username}).rowcount > 0


class UserHandler():
    def __init__(self, username, password):
        self._username = username
        self._password = password
    
    def register(self):
        if self._validate_username() and self._validate_password():
            user = User()
            try:
                user.create(self._username, self._password)
            except Exception as e:
                print(e)
        else:
            raise Exception('Invalid input')

    def _validate_username(self):
        if not self._username:
            return False
        return True
    
    def _validate_password(self):
        if not self._password:
            return False
        return True
    

    




def validate_input(user, password):
    if not user or not password:
        return False
    return True

    