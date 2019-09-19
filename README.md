# Project 1
There are no special libraries required beyond Flask and SQLAlchemy

The main app starts in application.py which handles all the incoming routes.

The project is made of "factories" and "models" which colorate to each other. So for example my "user_factory.py" will create the user object/model

Factories:
user_factiry.py - Handles all the logic related to user management, such as registration and login 
book_factiry.py - Handles all the logic related to the book search and interaction

The books import utility is implemented in import.py and is run with 'python3 import.py' - make sure the books.csv file is in the root directory of the module

errors.py holds custom exceptions to handle the various error cases such as wrong password, invlaid username etc.

