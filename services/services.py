from data import AccountsData, LibraryData, AuthorsData, BorrowInfoData
from model import User, Author, Book, BorrowInfo
from services import generate_unique_id
import json



class GlobalServices():
    number_of_users = 0

    def __init__(self, file='data/storage.json'):
        self.file = file

        # Ensures that there is only one instance per data types
        self.accounts_data = AccountsData()
        self.authors_data = AuthorsData()
        self.library_data = LibraryData()
        self.borrow_data = BorrowInfoData()

        with open(file, 'r') as f:
            self.data = json.load(f)

        # Shorthands for each data calls
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
    def detect_empty_values(self, values: list[str]):
        for value in values:
            if value is None or value == '':
                return True
        


    """ Checks if a book is available for borrow or not.

        RETURNS:
            bool: True if book is available for borrow, otherwise False. """
    def is_available(self, book_title: str):
        if self.detect_empty_values([book_title]):
            return 'Empty values detected'
        elif not self.exists(book_title=book_title):
            return 'Book not found'
        else:
            availability = self.library[book_title].get('is_available')
            if availability:
                return True
        return False
    

    """ Gets the list of users who borrowed the specified book and prints it.
        
        RETURNS:
            str: 'Done' if successful, otherwise it defaults to the two main checks (exists/empty_values) """
    def book_borrow_history(self, book_title: str):
        if self.detect_empty_values([book_title]):
            return 'Empty values detected'
        elif self.exists(book_title=book_title):
            return 'Book not found'

        print('LIST OF BORROWERS:')
        n = 0
        for borrower in self.borrow[book_title]:
            for field, value in self.borrow[book_title][borrower]:
                n += 1
                print(f'{n}. {borrower}')
                print(f'{field}: {value}\n')
        return 'Done'
        

    """ Gets the list of books borrowed by the specified user and prints the list.
        
        RETURNS:
            str: 'Done' if successful, otherwise it defaults to the two main checks (exists/empty_values). """        
    def user_borrow_history(self, username: str):
        if self.detect_empty_values([username]):
            return 'Empty values detected'
        elif self.exists(username=username):
            return 'User not found'
        
        print(f'LIST OF BOOKS BORROWED BY {username}:')
        n = 0
        for book in self.accounts['borrowed_books'].values():
            n +=1
            print(f'{n}. {book}')
        return 'Done'
    


    """ Searches for any relevant information regarding a particular item (book, user, author) and prints it.

        RETURNS:
            str: 'Done' if found, otherwise it defaults to the two main checks (exists/empty_values). """
    def get_info(self, what_to_search: str, name: str):
        if self.detect_empty_values([what_to_search, name]):
            return 'Empty values detected'

        if what_to_search.lower() not in ['user', 'book', 'author']:
            return 'Search invalid'
        
        if not self.exists(book_title=name):
            return 'Book not found'
        elif not self.exists(author_name=name):
            return 'Author not found'
        elif not self.exists(username=name):
            return 'User not found'
        else:
            print(f'YOU SEARCHED FOR: {name}')
            for field, info in self.accounts[name]:
                print(f'{field}: {info}')
        return 'Done'



    def get_books_written(self, author_name: str):
        ...



    @classmethod
    def total_user(self):
        ...

    @classmethod
    def total_active_user(self):
        ...

    @classmethod
    def total_number_of_books(self):
        ...







class LibrarianServices(GlobalServices):
    def __init__(self, file='data/storage.json'):
        super().__init__(file)


    # Account-related services
    def create_user(self, username, email, age):
        if self.detect_empty_values([username, email, age]):
            return 'Empty values detected'
        elif self.exists(username=username):
            return 'The username has already been taken.'
        elif age < 0 or age > 120:
            return 'Come on now, get serious. Ur not that old.'
        else:   
            existing_ids = {user['id'] for user in self.accounts.values()}
            id = generate_unique_id(existing_ids)
            new_user = User(username, email, age, id)
            self.accounts_data.create_data(new_user)

    def delete_user(self, username: str):
        if self.detect_empty_values([username]):
            return 'Empty value detected'
        elif not self.exists(username=username):
            return 'User not found'
        else:
            self.accounts_data.delete_data(username)

    def update_user(self, username, field, new_value):
        if self.detect_empty_values([username, field, new_value]):
            return 'Empty values detected'
        elif not self.exists(username=username):
            return 'User not found'
        elif not self.exists(field=field):
            return f'Invalid field: {field}'
        elif field == 'age' and not isinstance(new_value, int):
            return f'Age must only be expressed in numbers, not {new_value}'
        elif field == 'role' and new_value not in ['Member','Librarian']:
            return f'Invalid role: {new_value}'
        elif field == 'id':
            return 'Ids cannot be change'
        elif field == 'remaining_borrow':
            return 'Cannot change this field'
        else:
            user_changes = [username, field, new_value]
            self.accounts_data.update_data(user_changes)


    # Library-related services
    def add_book(self, book_title, author_name, quantity=1, date_published='Unknown', genre='Unknown', age_restriction='all-ages', is_available=True):
        if self.detect_empty_values([book_title, author_name]):
            return 'Empty values detected'
        elif self.exists(book_title=book_title):
            return 'Book already exists in the library'
        elif quantity < 0:
            return 'Book quantity cannot be less than zero'
        elif age_restriction != 'all-ages' and age_restriction != 'mature':
            return 'Enter a valid and proper age restriction'
        else:
            # adds the book to the library data
            new_book = Book(book_title, author_name, quantity, date_published, genre, age_restriction, is_available)
            self.library_data.create_data(new_book)

    def remove_book(self, book_title):
        if self.detect_empty_values([book_title]):
            return 'Empty values detected'
        elif not self.exists(book_title=book_title):
            return 'The book cannot be found'
        else:
            self.library_data.delete_data(book_title)

    def update_book(self, book_title, field, new_value):
        if self.detect_empty_values([book_title, field, new_value]):
            return 'Empty values detected'
        elif not self.exists(book_title=book_title):
            return 'Book not found'
        elif field == 'age_restriction' and new_value != 'mature' or new_value != 'all-ages':
            return 'Age restriction type cannot be anything other than all-ages or mature.'
        elif field == 'is_available' and not isinstance(new_value, bool):
            return 'Book availability must only be expressed as boolean (True/False)'
        elif (field == 'age' and not isinstance(new_value, int)) and new_value < 0:
            return 'Age must only be expressed in whole numbers greater than 0'
        elif not self.exists(field=field):
            return f'Invalid field entered: {field}'
        else:
            book_changes = [book_title, field, new_value]
            self.library_data.update_data(book_changes)


    # Borrow-related services
    def update_borrow_info(self, book_title, username, field, new_value):
        if self.detect_empty_values([book_title, username, field, new_value]):
            return 'Empty values detected'
        elif not self.exists(username=username):
            return 'User not found'
        elif field == 'user_status' and new_value != any('Active', 'Inactive', 'Removed', 'Deleted'):
            return 'User status changes invalid'
        elif not self.exists(field=field):
            return 'Field specified do not exist'
        elif not isinstance(new_value, str):
            return 'Must be in strings'
        else:
            return_info = [book_title, username,  field, new_value]
            self.borrow_data.update_data(return_info)

    def delete_borrow_info(self, book_title, username):
        if self.detect_empty_values([book_title, username]):
            return 'Empty values detected'
        elif not self.exists(username=username):
            return 'User not found'
        elif not self.exists(book_title=book_title):
            return 'Book not found'
        else:
            borrow_info = [book_title, username]
            self.borrow_data.delete_data(borrow_info)






class MemberServices(GlobalServices):
    def __init__(self, file='data/storage.json'):
        super().__init__(file)

    def borrow_book(self, book_title: str, username: str, borrowed_on: str, borrow_deadline: str):
        if self.detect_empty_values([username, book_title, borrowed_on, borrow_deadline]):
            return 'Empty values detected'
        elif not self.exists(book_title=book_title):
            return 'Book not found'
        elif not self.exists(username=username):
            return 'User not found'
        elif not isinstance(borrowed_on, str) or not isinstance(borrow_deadline, str):
            return 'Dates must be in strings'
        else:
            borrow_info = BorrowInfo(book_title, username, borrowed_on, borrow_deadline)
            self.borrow_data.create_data(borrow_info)

    def return_book(self, book_title, username, returned_on):
        if self.detect_empty_values([book_title, username, returned_on]):
            return 'Empty values detected'
        elif not self.exists(username=username):
            return 'User not found'
        elif not self.exists(book_title=book_title):
            return 'Book not found'
        elif not isinstance(returned_on, str):
            return 'Returned date must be string'
        else:
            return_info = [book_title, username,  'returned_on', returned_on]
            self.borrow_data.update_data(return_info)

