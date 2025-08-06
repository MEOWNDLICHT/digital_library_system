""" This is the MAIN LOGIC of the program, wherein the different CRUD-based operations are handled according to user roles.  """

from model import User, Author, Book, Borrow
from data import Create, Update, Delete
from check import Check
from error import EmptyValueError, NameTakenError, NameNotFoundError, InvalidAgeError, InvalidEmailError, InvalidChangeError
from generate_id import generate_unique_id
import json



class GeneralServices():
    def __init__(self, file='data/storage.json'):
        self.file = file

        with open(file, 'r') as f:
            self.data = json.load(f)

        # Ensures that each data methods have only one instance
        self.create = Create()
        self.update = Update()
        self.delete = Delete()
        self.check = Check()

        # Shorthands to ease each dataset calls
        self.accounts = self.data['accounts']
        self.library = self.data['library']
        self.borrow = self.data['borrows']
        self.authors = self.data['authors']

        # For tracking total numbers of users, books, and authors
        User.total_number = len(self.accounts)
        Book.total_number = len(self.library)
        Author.total_number = len(self.authors)



    """ Checks if a book is currently available for borrow
         RETURNS:
            bool: True if available, False otherwise.  """
    def is_available(self, title: str):
        book_is_available = self.library[title]['is_available']

        if self.check.detect_empty_values(title):
            raise EmptyValueError()
        elif not self.check.exists(book_title=title):
            raise NameTakenError(f"Book title '{title}' already taken!")
        elif book_is_available == False:
            print('Book unavailable for borrow.')
        else:
            print(f"Book requested '{title}' is available for borrow!")
            return True
        return False


    """ Searches for any relevant information regarding a particular item (book, user, author) and prints it.
        RETURNS:
            str: 'Success!' if found, otherwise None """
    def search(self, what_to_search: str, name:str):
        if self.check.detect_empty_values(what_to_search, name):
            raise EmptyValueError()
        elif what_to_search.lower() not in ['user', 'book', 'author']:
            print('Search invalid. Can only search for user, book, and author.')
            return 
        
        print(f'YOU SEARCHED FOR: {name}')
        match what_to_search:
            case 'user':
                if not self.check.exists(username=name):
                    print(f"User '{name}' cannot be found!")
                else:
                    for field, info in self.accounts[name]:
                        print(f'{field}: {info}')
                    return 'Success!'

            case 'book':
                if not self.check.exists(book_title=name):
                    print(f"Book '{name}' cannot be found!")
                else:
                    for field, info in self.library[name]:
                        print(f'{field}: {info}')
                    return 'Success!'

            case 'author':
                if not self.check.exists(author_name=name):
                    print(f"Author '{name}' cannot be found!")
                else:
                    for field, info in self.authors[name]:
                        print(f'{field}: {info}')
                    return 'Success!'


    """ Gets the list of books borrowed by the specified user and prints the list.
        RETURNS:
            str: 'Success!' if successful, otherwise None. """        
    def user_borrow_history(self, name: str):
        if self.check.detect_empty_values(name):
            raise EmptyValueError()
        elif not self.check.exists(username=name):
            raise NameNotFoundError(f"User '{name}' cannot be found!")
        
        print(f'LIST OF BOOKS BORROWED BY {name}:')
        for number, book in enumerate(self.accounts['borrowed_books'], start=1).values():
            print(f'{number}. {book}')
        return 'Successful!'


    """ Gets the list of users who borrowed the specified book and prints it.
        RETURNS:
            str: 'Successful!' if successful, otherwise None. """
    def book_borrow_history(self, title: str):
        if self.check.detect_empty_values(title):
            raise EmptyValueError()
        elif not self.check.exists(book_title=title):
            raise NameNotFoundError(f"Book '{title}' cannot be found!")

        print('LIST OF BORROWERS:')
        for number, borrower in enumerate(self.borrow[title], start=1):
            for field, value in self.borrow[title][borrower]:
                print(f'{number}. {borrower}')
                print(f'{field}: {value}\n')
            return 'Successful!'


    """ Gets all the books written by the specified author.
        RETURNS:
         list: All the books written by the author """
    def get_written_books(self, name: str):
        if self.check.detect_empty_values(name):
            raise EmptyValueError()
        elif not self.check.exists(author_name=name):
            raise NameNotFoundError(f"Author '{name}' cannot be found!")
        else:
            books_written = self.authors[name]['books']
            for books in books_written:
                for number, book in enumerate(books):
                    print(number, book)
        return books_written


    """ Gets the total number of accounts created in the program.
        RETURNS:
            int: The total number of users """
    @classmethod
    def user_metrics(cls):
        print(f'The total number of users are: {User.total_number}')
        return User.total_number


    """ Gets the total number of books added to the library.
        RETURNS:
            int: The total number of books in the library. """
    @classmethod
    def book_metrics(cls):
        print(f'The total number of books in the library are: {Book.total_number}')
        return Book.total_number




class LibrarianServices(GeneralServices):
    pass



class MemberServices(GeneralServices):
    pass