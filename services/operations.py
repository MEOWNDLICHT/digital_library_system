""" This is the MAIN LOGIC of the program, wherein the different CRUD-based operations are handled according to user roles.  """

from model import User, Author, Book, Borrow
from data import Create, Update, Delete
from .validation import Check
from .error import EmptyValueError, NameTakenError, NameNotFoundError, InvalidAgeError, InvalidEmailError, InvalidChangeError, InvalidQuantityError, BookUnavailableError
from .generate_id import generate_unique_id
from datetime import datetime, timedelta
import json
import os



class GeneralServices():
    DEFAULT_DATASETS = {'accounts': {}, 
                        'authors': {},
                        'library': {},
                        'borrows': {}}


    def __init__(self, file='data/storage.json'):
        self.file = file

        # checks if the json file exists and sets the default data structures
        if not os.path.exists(file):
            with open(file, 'w') as create_file:
                json.dump(self.DEFAULT_DATASETS, create_file, indent=4)

        try:
            with open(file, 'r') as f:
                self.data = json.load(f)

        # To ensure that the program wouldn't break regardless of whether storage.json is empty or cannot be found.
        except (json.JSONDecodeError, FileNotFoundError):
            self.data = self.DEFAULT_DATASETS.copy()

        # Ensures that each data methods have only one instance and all are synched (or uses the same 'data')
        self.create = Create(self.data, self.file)
        self.update = Update(self.data, self.file)
        self.delete = Delete(self.data, self.file)
        self.check = Check(self.data, self.file)

        # Shorthands to ease each dataset calls
        self.accounts = self.data['accounts']
        self.library = self.data['library']
        self.borrow = self.data['borrows']
        self.authors = self.data['authors']

        # For tracking total numbers of users, books, and authors
        User.total_number = len(self.accounts)
        Book.total_number = len(self.library)
        Author.total_number = len(self.authors)



    def is_available(self, title: str):
        """ Checks if a book is available for borrow.

            Returns:
                bool: True if available, otherwise False. """
        book_is_available = self.library[title]['is_available']

        if self.check.detect_empty_values(title):
            raise EmptyValueError()
        elif not self.check.exists(book_title=title):
            raise NameTakenError(title)
        elif book_is_available == False:
            raise BookUnavailableError(title)
        else:
            print(f"Book requested, '{title}', is available for borrow!")
            return True


    def search(self, what_to_search: str, name:str):
        """ Searches for any relevant information regarding a particular item (book, user, author) and prints it.
            
            Returns:
                str: 'Success!' if found, otherwise None."""
        if self.check.detect_empty_values(what_to_search, name):
            raise EmptyValueError()
        elif what_to_search.lower() not in ['user', 'book', 'author']:
            print('Search invalid. Can only search for user, book, and author.')
            return 
        
        print(f'\nYOU SEARCHED FOR: {name}\n')
        match what_to_search:
            case 'user':
                if not self.check.exists(username=name):
                    raise NameNotFoundError(username=name)
                else:
                    for field, info in self.accounts[name].items():
                        print(f'{field.capitalize().replace('_', ' ')}: {info}')
                    return 'Success!'

            case 'book':
                if not self.check.exists(book_title=name):
                    raise NameNotFoundError(book_title=name)
                else:
                    for field, info in self.library[name].items():
                        print(f'{field.capitalize().replace('_', ' ')}: {info}')
                    return 'Success!'

            case 'author':
                if not self.check.exists(author_name=name):
                    raise NameNotFoundError(author=name)
                else:
                    for field, info in self.authors[name].items():
                        print(f'{field.capitalize().replace('_', ' ')}: {info}')
                    return 'Success!'


    def user_borrow_history(self, name: str):
        """ Gets the list of books borrowed by the specified user and prints the list.  
            
            Returns:
                str: 'Success!' if successful, otherwise None."""   
        if self.check.detect_empty_values(name):
            raise EmptyValueError()
        elif not self.check.exists(username=name):
            raise NameNotFoundError(username=name)
        
        print(f'LIST OF BOOKS BORROWED BY {name}:')
        for number, book in enumerate(self.accounts['borrowed_books'], start=1).values():
            print(f'{number}. {book}')
        return 'Successful!'


    def book_borrow_history(self, title: str):
        """ Gets the list of users who borrowed the specified book and prints it.  
            
            Returns:
                str: 'Successful!' if successful, otherwise None."""
        if self.check.detect_empty_values(title):
            raise EmptyValueError()
        elif not self.check.exists(book_title=title):
            raise NameNotFoundError(book_title=title)
        elif not self.check.exists(borrow_bookname=title):
            raise NameNotFoundError(borrowed_book=title)

        print('LIST OF BORROWERS:')
        for number, borrower in enumerate(self.borrow[title], start=1):
            for field, value in self.borrow[title][borrower]:
                print(f'{number}. {borrower}')
                print(f'{field}: {value}\n')
            return 'Successful!'


    def get_written_books(self, name: str):
        """ Gets all the books written by the specified author.  
            
            Returns:
                list: All the books written by the author. """
        if self.check.detect_empty_values(name):
            raise EmptyValueError()
        elif not self.check.exists(author_name=name):
            raise NameNotFoundError(author=name)
        else:
            books_written = self.authors[name]['books']
            for books in books_written:
                for number, book in enumerate(books):
                    print(number, book)
        return books_written


    @classmethod
    def user_metrics(cls):
        """ Gets the total number of accounts created in the program.
        
            Returns:
                int: The total number of users. """
        print(f'The total number of users are: {User.total_number}')
        return User.total_number


    @classmethod
    def book_metrics(cls):
        """ Gets the total number of books added to the library.

            Returns:
                int: The total number of books in the library. """
        print(f'The total number of books in the library are: {Book.total_number}')
        return Book.total_number




class LibrarianServices(GeneralServices):
    def __init__(self, file='data/storage.json'):
        super().__init__(file)

    """ USER-RELATED OPERATIONS """
    def create_user(self, user_name: str, user_email: str, user_age: int):
        if self.check.detect_empty_values(user_name, user_email, user_age):
            raise EmptyValueError()
        elif self.check.exists(user_name):
            raise NameTakenError('user', user_name)
        elif not self.check.is_valid(email=user_email):
            raise InvalidEmailError()
        else:
            # generates a random unique id for the user
            existing_ids = {user['id'] for user in self.accounts.values()}
            id = generate_unique_id(existing_ids)
            
            # creates user object
            new_user = User(user_name, user_email, user_age, id)

            # increments the total number of users in the program by 1
            User.total_number += 1

            # save to json
            self.create.save_user(new_user)


    def update_user(self, name, field_name, new_value):
        changes =  ['accounts', name, field_name, new_value]

        if self.check.detect_empty_values(changes):        
            raise EmptyValueError()
        elif not self.check.exists(username=name):
            raise NameNotFoundError(username=name)
        elif not self.check.field_exists(field=field_name):
            raise NameNotFoundError(field=field_name)
        elif field_name == 'age' and not self.check.is_valid(age=new_value):
            raise InvalidAgeError()
        elif field_name == 'role' and not self.check.is_valid(role=new_value):
            raise InvalidChangeError('role')
        elif field_name in ['id', 'remaining_borrow']:
            raise InvalidChangeError('field', field_name)
        else:
            # update and save changes to json
            self.update.update_entry(changes)


    def remove_user(self, name: str):
        user_entry = ['accounts', name]

        if self.check.detect_empty_values(name):        
            raise EmptyValueError()
        elif not self.check.exists(username=name):
            raise NameNotFoundError(username=name)
        else:
            self.delete.delete_entry(user_entry)


    """ LIBRARY-RELATED OPERATIONS """
    def add_book(self, title:str, author: str, quantity=1, date_published='unknown', genre='unknown', age_restriction='all-ages', is_available=True):
        if self.check.detect_empty_values(title, author, quantity, date_published, genre, age_restriction, is_available):
            raise EmptyValueError()
        elif self.check.exists(title):
            raise NameTakenError('book', title)
        elif quantity < 0:
            raise InvalidQuantityError('quantity_less_than_zero')
        elif not self.check.is_valid(quantity=quantity):
            raise InvalidQuantityError('quantity_not_int')
        else:       
            new_book = Book(title, author, quantity, date_published, genre, age_restriction, is_available)

            # adds author to the database if new.
            if author not in self.authors:
                new_author = Author(author, books=[title])
                self.create.save_author(new_author)
        
            # updates the author's written books list.
            written_books = self.data['authors'][author]['books']
            if title not in written_books:
                written_books.append(title)
                self.update.update_entry(['authors', author, 'books', written_books])

            # saves the new book to the database
            self.create.save_book(new_book)


    def update_book(self, title: str, field_name: str, new_value):
        changes =  ['library', title, field_name, new_value]

        if self.check.detect_empty_values(title, field_name, new_value):
            raise EmptyValueError()
        elif not self.check.exists(book_title=title):
            raise NameNotFoundError(book_title=title)
        elif not self.check.field_exists(field=field_name):
            raise NameNotFoundError(field=field_name)
        elif field_name == 'quantity' and new_value < 0:
            raise InvalidQuantityError('quantity_less_then_zero')
        elif field_name == 'quantity' and not self.check.is_valid(quantity=new_value):
            raise InvalidQuantityError('quantity_not_int')
        elif field_name == 'age_restriction' and new_value not in ['all-ages', 'mature']:
            raise InvalidChangeError('field', field_name, new_value)
        elif field_name == 'is_available' and not self.check.is_valid(is_available=new_value):
            raise ValueError(f"Field, '{field_name}', must be a string data type.")
        else:
            self.update.update_entry(changes)


    def remove_book(self, title: str):
        book_entry = ['library', title]

        if self.check.detect_empty_values(title):
            raise EmptyValueError()
        elif not self.check.exists(book_title=title):
            raise NameNotFoundError(book_title=title)
        else:
            self.delete.delete_entry(book_entry)


    """ AUTHOR-RELATED OPERATIONS """
    def update_author(self, name: str, field_name: str, new_value: str):
        changes = ['authors', name, field_name, new_value]

        if self.check.detect_empty_values(name, field_name, new_value):
            raise EmptyValueError()
        elif not self.check.exists(name):
            raise NameNotFoundError(author=name)
        elif not self.check.exists(field=field_name):
            raise NameNotFoundError(field=field_name)
        elif field_name  == 'books':
            raise InvalidChangeError('books list', field_name)
        elif field_name == 'age' and not self.check.is_valid(new_value):
            raise InvalidAgeError()
        else:
            self.update.update_entry(changes)


    """ BORROW-RELATED OPERATIONS """
    def update_borrow(self, title: str, borrower: str, field_name: str, new_value: str):
        changes = [title, borrower, field_name, new_value]

        if self.check.detect_empty_values(title, borrower, field_name, new_value):
            raise EmptyValueError()
        elif not self.check.exists(book_title=title):
            raise NameNotFoundError(book_title=title)
        elif not self.check.exists(username=borrower):
            raise NameNotFoundError(username=borrower)
        
        # checks if the book title and borrower exists in the borrow database.
        elif not self.check.exists(borrow_bookname=title):
            raise NameNotFoundError(borrowed_book=title)
        elif not self.check.exists(borrow_username=borrower):
            raise NameNotFoundError(borrower=borrower)

        elif not self.check.field_exists(field=field_name):
            raise NameNotFoundError(field=field_name)
        elif field_name == 'borrow_deadline' or field_name == 'borrowed_on':
            raise InvalidChangeError('field', field_name)
        else:
            self.update.update_borrow(changes)
        



class MemberServices(GeneralServices):
    """ BORROW-RELATED OPERATIONS FOR MEMBERS """
    def borrow_book(self, title: str, borrower: str):
        # generates the date today
        borrowed_on = datetime.now()

        # sets a two-week deadline for borrowed_on
        borrow_deadline = borrowed_on + timedelta(days=14)

        if self.check.detect_empty_values(title, borrower):
            raise EmptyValueError()
        elif not self.check.exists(book_title=title):
            raise NameNotFoundError(book_title=title)
        elif not self.check.exists(username=borrower):
            raise NameNotFoundError(username=borrower)
        elif not self.library[title]['is_available']:
            raise BookUnavailableError(title)
        else:
            # # this makes the dates readable (format: weekday_name, month_name day, year)
            # returned_on = returned_on.strftime("%A, %B %d, %Y")
            # borrow_deadline = borrow_deadline.strftime("%A, %B %d, %Y")

            # creates the borrow object and saves it to the database.
            new_borrow = Borrow(title, borrower, borrowed_on, borrow_deadline)
            self.create.save_borrow(new_borrow)
    

    def return_book(self, title: str, borrower: str):
        if self.check.detect_empty_values(title, borrower):
            raise EmptyValueError()
        elif not self.check.exists(book_title=title):
            raise NameNotFoundError(book_title=title)
        elif not self.check.exists(username=borrower):
            raise NameNotFoundError(username=borrower)
        
        # checks if the book title and borrower exists in the borrow database.
        elif not self.check.exists(borrow_bookname=title):
            raise NameNotFoundError(borrowed_book=title)
        elif not self.check.exists(borrow_username=borrower):
            raise NameNotFoundError(borrower=borrower)
        else:
            returned_date = datetime.now()
            return_info = [title, borrower, 'returned_on', returned_date]
            self.update.update_borrow(return_info)