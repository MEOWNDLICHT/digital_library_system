from data import AccountsData, AuthorsData, LibraryData, BorrowInfoData
import json


class Check:
    def __init__(self, file='data/storage.json'):
        self.file = file

        with open(file, 'r') as f:
            self.data = json.load(f)

        # Shorthands to ease of data calls
        self.accounts = self.data['accounts']
        self.library = self.data['library']
        self.borrow = self.data['borrow_data']
        self.authors = self.data['authors']


    """Checks to see if there are any empty values detected in the input
        
        RETURNS:
            bool: True if any empty input values are detected, otherwise False. """
    @staticmethod
    def detect_empty_values(values: list[str]):
        if any(value == "" for value in values):
            return True
        return False


    """ Checks for the existence of an item in the dataset.
        
        NOTE: it is REQUIRED to specify the parameter name before entering the value u want to check 
        sample: (username = name_of_user). 
        
        RETURNS:
            bool: True if item found (or exists), otherwise False. """
    def exists(self, username=None, book_title=None, author_name=None, borrow_info=None, field=None):

        if username in self.accounts:
            return True
        if book_title in self.library:
            return True
        if author_name in self.authors:
            return True
        if borrow_info in self.borrow:
            return True
        
        # This only works for the first three datasets: accounts, library, and authors
        for dataset in self.data.values():
            for names in dataset.values():
                if field in names.keys():
                    return True

        # Borrow data has a very specific structure
        for title in self.borrow:
            for borrowers in self.borrow[title]:
                if field in self.borrow[title][borrowers].keys():
                    return True
        return False
    

    """ Checks if a value that the user has given is valid
     
        RETURN:
            bool: True if valid, False otherwise. """
    def is_valid(self, name=None, email=None, role=None, age=None):
        if not isinstance(name, str):
            return False
        elif not isinstance(age, int):
            return False
        elif not isinstance(email, str):
            return False
        elif isinstance(role, str):
            return False
        
        # age validation
        elif age < 13 or age > 120:
            return False
        
        # email validation
        elif '@' not in email:
            return False
        elif email.split('@')[1].lower() not in ['gmail.com', 'yahoo.com']:
            return False
        
        # role validation
        elif role.lower() not in ['librarian', 'member']:
            return False
        return True
        



# List of all exceptions and errors
class Error(Exception):
    ...

class EmptyValueError(Error):
    """ if an empty value is detected upon calling a method, this'll be called. """
    ...

class NameTaken(Error):
    """ if an user's, author's, or book's name has already been taken, this'll be called. """
    ...

class NotFound(Error):
    """ if an user's, author's, or book's name cannot be found in the database, this'll be called. """
    ...

class InvalidAge(Error):
    """ if an age value is higher (>125) or lower (<13) than the age limit, this'll be called. """
    ...

class InvalidChange(Error):
    """ if the user tries to change something in a sensitive field, this'll be called. """
    ...

