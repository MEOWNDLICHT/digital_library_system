from model import Book, User, Author
from data import AccountsData, AuthorsData, LibraryData, BorrowData
from services import generate_unique_id
from error_handling import Check, NotFound, NameTaken, EmptyValueError, InvalidAge, InvalidChange
import json



class GeneralServices():
    def __init__(self, file='data/storage.json'):
        self.file = file

        # Ensures that there is only one instance per data
        self.accounts_data = AccountsData()
        self.authors_data = AuthorsData()
        self.library_data = LibraryData()
        self.borrow_data = BorrowData()

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
            raise EmptyValueError('Empty value detected.')
        elif not Check.exists(book_title=title):
            raise NameTaken('Book title already taken!')
        elif self.library[title]['is_available'] == False:
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
            raise EmptyValueError('Empty value detected.')
        elif what_to_search.lower() not in ['user', 'book', 'author']:
            print('Search invalid. Can only search for user, book, and author.')
            return 
        
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


    """ Gets the list of books borrowed by the specified user and prints the list.
        RETURNS:
            str: 'Success!' if successful, otherwise None. """        
    def user_borrow_history(self, name: str):
        if Check.detect_empty_values([name]):
            raise EmptyValueError('Empty values detected')
        elif not Check.exists(username=name):
            raise NotFound('User cannot be found!')
        
        print(f'LIST OF BOOKS BORROWED BY {name}:')
        for number, book in enumerate(self.accounts['borrowed_books'], start=1).values():
            print(f'{number}. {book}')
        return 'Successful!'


    """ Gets the list of users who borrowed the specified book and prints it.
        RETURNS:
            str: 'Successful!' if successful, otherwise None. """
    def book_borrow_history(self, title: str):
        if Check.detect_empty_values([title]):
            raise EmptyValueError('Empty values detected')
        elif not Check.exists(book_title=title):
            raise NotFound('Book cannot be found!')

        print('LIST OF BORROWERS:')
        for number, borrower in enumerate(self.borrow[title], start=1):
            for field, value in self.borrow[title][borrower]:
                print(f'{number}. {borrower}')
                print(f'{field}: {value}\n')
            return 'Successful!'


    """ Gets all the books written by the specified author.
        RETURNS:
         list: All the books written by the author """
    def get_written_books(self, author: str):
        if Check.detect_empty_values(author):
            raise EmptyValueError('Empty value detected!')
        elif not Check.exists([author]):
            raise NotFound('Author cannot be found!')
        else:
            books_written = self.authors[author]['books']
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
    def __init__(self, file='data/storage.json'):
        super().__init__(file)


    def create_user(self, name: str, email: str, age: int):
        if Check.detect_empty_values([name, email, age, id]):
            raise EmptyValueError('Emtpy values detected')
        elif Check.exists(name):
            raise NameTaken('Username already taken!')
        else:
            User.total_number += 1

            # generates a random unique id for the user
            existing_ids = {user['id'] for user in self.accounts.values()}
            id = generate_unique_id(existing_ids)
            
            # creates and save the user to json
            new_user = User(name, email, age, id)
            self.accounts_data.create_data(new_user)
            self.accounts_data.save_changes()


    def update_user(self, name, field, new_value):
        changes =  [name, field, new_value]

        if Check.detect_empty_values(changes):        
            raise EmptyValueError('Empty value detected!')
        elif not Check.exists(username=name):
            raise NotFound('User cannot be found!')
        elif not Check.exists(field=field):
            raise NotFound('Field cannot be found!')
        elif field == 'age' and Check.is_valid(age=new_value):
            raise InvalidAge('Age entered is invalid. Either too old, too young, or not real.')
        elif field == 'role' and Check.is_valid(role=new_value):
            raise InvalidChange('Role invalid. Roles must only be librarian/member.')
        elif field == 'id':
            raise InvalidChange('IDs cannot be change.')
        elif field == 'remaining_borrow':
            raise InvalidChange('This must not be change at all cost.')
        else:
            # update and save changes to json
            self.accounts_data.update_data(changes)
            self.accounts_data.save_changes()


    def delete_user(self, name: str):
        User.total_number -= 1

        if Check.detect_empty_values([name]):
            raise EmptyValueError('Empty value detected!')
        elif not Check.exists(name):
            raise NotFound('User cannot be found!')
        else:
            # deletes the entry from json and save the changes
            self.accounts_data.delete_data(name)
            self.accounts_data.save_changes()

    
    def add_book(self, title:str, author: str, quantity=1, date_published='unknown', genre='unknown', age_restriction='all-ages', is_available=True):
        if Check.detect_empty_values([title, author, quantity, date_published, genre, age_restriction, is_available]):
            raise EmptyValueError('Empty values detected!')
        elif Check.exists([title]):
            raise NameTaken('Book title already taken!')
        elif quantity < 0:
            raise ValueError('Book quantity cannot be lower than zero.')
        else:
            User.total_number+= 1
            Author.total_number += 1

            self.data.save_changes()


    def update_book(self, title, field, new_value):
        ...


    def delete_book(self, title: str):
        Book.total_number -= 1


    def update_author(self, name, field, new_value):
        ...


    def remove_author(self, name: str):
        Author.total_number -= 1


    def edit_borrow_info(self, book: str, name: str, field: str, new_value: str):
        ...




class MemberServices(GeneralServices):
    def __init__(self, file='data/storage.json'):
        super().__init__(file)

    def borrow_book(self, title: str, user_name: str):
        ...

    def return_book(self, title: str, user_name: str):
        ...