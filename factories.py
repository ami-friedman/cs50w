from models import User

class UserFactory:
    def create(username, password):
        self._username = username
        self._password = password
        if not self._is_username_exists():
            self._create()
        else:
            raise Exception('User already exists')

class BookFactory:
    pass

class ReviewFactory:
    pass