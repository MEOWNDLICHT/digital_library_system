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
        
        # This only works for the first three data types: accounts, library, and authors
        for data_type in self.data:
            if field in self.data[data_type]:
                return True
        
        # Borrow data has a very specific structure (also see: BorrowInfoData class from store_data.py)
        for book_title in self.borrow:
            for borrowers in self.borrow[book_title]:
                if field in self.borrow[book_title][borrowers]:
                    return True
        return False
    

    """Checks to see if there are any empty values detected in the input
        
        RETURNS:
            bool: True if any empty input values are detected, otherwise False. """
    @staticmethod
    def detect_empty_values(values: list[str]):
        if any(value == "" for value in values):
            return True
        return False
    

    def valid_field(self, field_type: str):
        ...


    def is_valid(self, name=None, email=None, role=None, age=None):
        ...



# List of all exceptions and errors
class Error(Exception):
    ...

class EmptyValueError(Error):
    ...

class NameTaken(Error):
    ...

class NotFound(Error):
    ...

class InvalidAge(Error):
    ...

class InvalidField(Error):
    ...
