from model import Book, User, Author, BorrowInfo
from abc import ABC, abstractmethod
import json
import os


class DataHandling(ABC):
     DEFAULT_DATA_STRUCTURE = {
          "accounts": {},
          "library": {},
          "authors": {},
          "borrow_data": {}
     }
          
     def __init__(self, file='data/storage.json'):
          self.file = file

          # Checks if the json file exists and sets the default data structures
          if not os.path.exists(file):
               with open(file, 'w') as create_file:
                    json.dump(self.DEFAULT_DATA_STRUCTURE, create_file, indent=4)
          
          try:
               with open(file, 'r') as f:
                    self.data = json.load(f)
          
          # To ensure that it wouldnt break regardless of whether storage.json is empty or not.
          except json.JSONDecodeError:
            self.data = self.DEFAULT_DATA_STRUCTURE.copy()
            self.save_changes()

        
     @abstractmethod
     def create_data(self, data):
         ...

     @abstractmethod
     def delete_data(self, data):
          ...

     @abstractmethod
     def update_data(self, data):
         ...

     def save_changes(self):
          with open(self.file, 'w') as save_changes:
               json.dump(self.data, save_changes, indent=4)
        


class AccountsData(DataHandling):
     def __init__(self):
          super().__init__()
          
     def create_data(self, user: User):
          self.data['accounts'][user.username] = {'email': user.email,
                                      'age': user.age,
                                      'id': user.id,
                                      'role': user.role,
                                      'remaining_borrows': user.remaining_borrow,
                                      'borrow_limit': user.borrow_limit,
                                      'borrowed_books': user.borrowed_books}

     def delete_data(self, username: str):
          self.data['accounts'].pop(username)

     def update_data(self, data: list[str]):
          username, field, new_value = data
          self.data['accounts'][username][field] = new_value
         
          

class LibraryData(DataHandling):
     def __init__(self):
          super().__init__()

     def create_data(self, book: Book):
         self.data['library'][book.title] = {'author': book.author,
                                  'quantity': book.quantity,
                                  'date_published': book.date_published,
                                  'genre': book.genre,
                                  'age_restriction': book.age_restriction,
                                  'is_available': book.is_available}

     def delete_data(self, book_title: str):
          self.data['library'].pop(book_title)
    
     def update_data(self, data: list[str]):
          book_title, field, new_value = data
          self.data['library'][book_title][field] = new_value



class AuthorsData(DataHandling):
     def __init__(self):
          super().__init__()

     def create_data(self, author: Author):
         self.data['authors'][author.name] = {'age': author.age,
                                   'birthday': author.birthday,
                                   'nationality': author.nationality,
                                   'books': author.books}


     def delete_data(self, author_name):
          self.data['authors'].pop(author_name)

     def update_data(self, data: list[str]):
          author_name, field, new_value = data
          self.data['authors'][author_name][field] = new_value



class BorrowData(DataHandling):
     def __init__(self):
          super().__init__()

     def create_data(self, borrow: BorrowInfo):
          # Creates an entry for the book title so it doesnt break when there is nothing yet in the 'borrow storage layer'
          self.data['borrow_data'].setdefault(borrow.book_title, {})

          self.data['borrow_data'][borrow.book_title][borrow.borrowed_by] = {
               'user_status': borrow.user_status,
               'borrowed_on': borrow.borrowed_on,
               'borrow_deadline': borrow.borrow_deadline,
               'returned_on': borrow.returned_on}
          
     def delete_data(self, data: list[str]):
          book_title, borrower = data
          self.data['borrow_data'][book_title].pop(borrower)

     def update_data(self, data: list[str]):
          book_title, borrower, field, new_value = data
          self.data['borrow_data'][book_title][borrower][field] = new_value
          