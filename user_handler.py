from user import User
import sys, traceback

class UserHandler():
    def __init__(self, username, password):
        self._username = username
        self._password = password
        print(self._username, self._password)
    
    def register(self):
        if self._validate_username() and self._validate_password():
            user = User()
            try:
                user.create(self._username, self._password)
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
        else:
            raise Exception('Invalid input')

    def login(self):
        if self._validate_username() and self._validate_password():
            user = User(self._username, self._password)
            return user.login()
        return None

    def _validate_username(self):
        if not self._username:
            return False
        return True
    
    def _validate_password(self):
        if not self._password:
            return False
        return True