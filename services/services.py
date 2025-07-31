from data import AccountsData, LibraryData, AuthorsData, BorrowInfoData
from data import AccountsData, AuthorsData, LibraryData, BorrowInfoData
from services import generate_unique_id, Check
import json



class GeneralServices():
    number_of_users = 0

    def __init__(self, file='data/storage.json'):
        self.file = file

        # Ensures that there is only one instance per data
        self.accounts_data = AccountsData()
        self.authors_data = AuthorsData()
        self.library_data = LibraryData()
        self.borrow_data = BorrowInfoData()

        with open(file, 'r') as f:
            self.data = json.load(f)

        # Shorthands to ease of data calls
        self.accounts = self.data['accounts']
        self.library = self.data['library']
        self.borrow = self.data['borrow_data']
        self.authors = self.data['authors']


    """ Checks if a book is currently available for borrow

         RETURNS:
            bool: True if available, False otherwise.  """
    def is_available(self, title: str):
        if Check.detect_empty_values(title):
            print('Empty value detected.')
        elif not Check.exists(book_title=title):
            print('Book cannot be found!')
        elif self.library[title]['is_available'] == 'False':
            print('Book cannot be borrowed for the time being.')
        else:
            print(f"Book requested '{title}' is available for borrow!")
            return True
        return False


    """ Searches for any relevant information regarding a particular item (book, user, author) and prints it.

        RETURNS:
            str: 'Success!' if found, otherwise None """
    def search(self, what_to_search: str, name:str):
        if Check.detect_empty_values([what_to_search]):
            print('Empty value detected.')
        elif what_to_search.lower() not in ['user', 'book', 'author']:
            print('Search invalid. Can only search for user, book, and author.')
        print(f'YOU SEARCHED FOR: {name}')

        match what_to_search:
            case 'user':
                if not Check.exists(username=name):
                    print('User cannot be found!')
                else:
                    for field, info in self.accounts[name]:
                        print(f'{field}: {info}')
                    return 'Success!'

            case 'book':
                if not Check.exists(book_title=name):
                    print('Book cannot be found!')
                else:
                    for field, info in self.library[name]:
                        print(f'{field}: {info}')
                    return 'Success!'

            case 'author':
                if not Check.exists(author_name=name):
                    print('Author cannot be found!')
                else:
                    for field, info in self.authors[name]:
                        print(f'{field}: {info}')
                    return 'Success!'
        return 


    """ Gets the list of books borrowed by the specified user and prints the list.
        
        RETURNS:
            str: 'Success!' if successful, otherwise None. """        
    def user_borrow_history(self, name: str):
        if self.detect_empty_values([name]):
            print('Empty values detected')
            return
        elif self.exists(username=name):
            print('User not found')
            return
        
        print(f'LIST OF BOOKS BORROWED BY {name}:')
        for number, book in enumerate(self.accounts['borrowed_books'], start=1).values():
            print(f'{number}. {book}')
        return 'Successful!'



    """ Gets the list of users who borrowed the specified book and prints it.
        
        RETURNS:
            str: 'Successful!' if successful, otherwise None. """
    def book_borrow_history(self, title: str):
        if Check.detect_empty_values([title]):
            print('Empty values detected')
        elif not Check.exists(book_title=title):
            print('Book not found')

        print('LIST OF BORROWERS:')
        for number, borrower in enumerate(self.borrow[title], start=1):
            for field, value in self.borrow[title][borrower]:
                print(f'{number}. {borrower}')
                print(f'{field}: {value}\n')
            return 'Successful!'
        return
        
    def get_written_books(self, author: str):
        ...


    @classmethod
    def user_metrics(cls):
        ...

    @classmethod
    def book_metrics(cls):
        ...





class LibrarianServices(GeneralServices):
    def __init__(self, file='data/storage.json'):
        super().__init__(file)

    def create_user(self):
        ...

    def update_user(self, name, field, new_value):
        ...

    def delete_user(self, name: str):
        ...

    
    def add_book(self, title:str, author: str):
        ...

    def update_book(self, title, field, new_value):
        ...

    def delete_book(self, title: str):
        ...

    def update_author(self, name, field, new_value):
        ...

    def edit_borrow_info(self, book: str, name: str, field: str, new_value: str):
        ...





class MemberServices(GeneralServices):
    def __init__(self, file='data/storage.json'):
        super().__init__(file)

    def borrow_book(self, title: str, user_name: str):
        ...

    def return_book(self, title: str, user_name: str):
        ...