from data import AccountsData, AuthorsData, LibraryData, BorrowData
import json


class Check:
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
    @staticmethod
    def exists(username=None, book_title=None, author_name=None, borrow_info=None, field=None, file='data/storage.json'):
        # Read and parses the json everytime the method is called, which might decrease performance.
        with open(file, 'r') as f:
            data = json.load(f)
        
        # Shorthands to ease of data calls
        accounts = data['accounts']
        library = data['library']
        authors = data['authors']
        borrow = data['borrow_data']


        if username in accounts:
            return True
        if book_title in library:
            return True
        if author_name in authors:
            return True
        if borrow_info in borrow:
            return True
        
        # This only works for the first three datasets: accounts, library, and authors
        for dataset in data.values():
            for names in dataset.values():
                if field in names.keys():
                    return True

        # borrow dataset has a very specific structure
        for title in borrow:
            for borrowers in borrow[title]:
                if field in borrow[title][borrowers].keys():
                    return True
        return False
    

    """ Checks if a value that the user has given is valid
        RETURN:
            bool: True if valid, False otherwise. """
    @staticmethod
    def is_valid(name='unknown', email='sample@gmail.com', role='member', age=18):
        if not isinstance(name, str):
            return False
        if not isinstance(age, int):
            return False
        if not isinstance(email, str):
            return False
        if not isinstance(role, str):
            return False
        
        # age validation
        if age < 13 or age > 120:
            return False
        
        # email validation
        if '@' not in email:
            return False
        elif email.split('@')[1].lower() not in ['gmail.com', 'yahoo.com']:
            return False
        
        # role validation
        if role.lower() not in ['librarian', 'member']:
            return False
        return True
        



# List of all exceptions and errors
class Error(Exception):
    ...

class EmptyValueError(Error):
    """ if an empty value is detected upon calling a method, this'll be called. """
    def __init__(self):
        super().__init__('Emtpy values detected')

class NameTaken(Error):
    """ if an user's, author's, or book's name has already been taken, this'll be called. """
    ...
    
class NotFound(Error):
    """ if an user's, author's, or book's name cannot be found in the database, this'll be called. """
    ...

class InvalidAge(Error):
    """ if an age value is higher (>125) or lower (<13) than the age limit, this'll be called. """
    def __init__(self):
        super().__init__("Invalid age. Either too old or too young! ")

class InvalidChange(Error):
    """ if the user tries to change something in a sensitive field, this'll be called. """
    ...

class InvalidEmail(Error):
    """ if the user tries to use an email that is not '@gmail.com' or '@yahoo.com', this gets called. """
    ...

