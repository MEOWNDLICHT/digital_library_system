""" This is where data is handled for different CRUD operations. All info are stored in json file. """

from model import User, Book, Author, Borrow
from abc import ABC
import os
import json



class GeneralDataHandling(ABC):
    DEFAULT_DATASETS = {
        'accounts': {},
        'authors': {},
        'library': {},
        'borrows': {}
    }

    def __init__(self, file='data/storage.json'):
        # Checks if the json file exists and sets the default data structures
        if not os.path.exists(file):
            with open(file, 'w') as create_file:
                json.dump(self.DEFAULT_DATASETS, create_file, indent=4)
        
        try:
            with open(file, 'r') as f:
                self.data = json.load(f)
          
        # To ensure that the program wouldn't break regardless of whether storage.json is empty or cannot be found.
        except (json.JSONDecodeError, FileNotFoundError):
            self.data = self.DEFAULT_DATASETS.copy()
            self.save_changes()


    def save_changes(self, file='data/storage.json'):
        with open(file, 'w') as save:
            json.dump(self.data, save, indent=4)
        




class Create(GeneralDataHandling):
    def __init__(self, file='data/storage.json'):
        super().__init__(file)

    def save_user(self, user: User):
        self.data['accounts'][user.username] = {'email': user.email,
                                                'age': user.age,
                                                'id': user.id,
                                                'role': user.role,
                                                'remaining_borrows': user.remaining_borrow,
                                                'borrow_limit': user.borrow_limit,
                                                'borrowed_books': user.borrowed_books}
        self.save_changes()

    def save_author(self, author: Author):
        self.data['authors'][author.name] = {'age': author.age,
                                            'birthday': author.birthday,
                                            'nationality': author.nationality,
                                            'books': author.books}
        self.save_changes()

    def save_book(self, book: Book):
        self.data['library'][book.title] = {'author': book.author,
                                            'quantity': book.quantity,
                                            'date_published': book.date_published,
                                            'genre': book.genre,
                                            'age_restriction': book.age_restriction,
                                            'is_available': book.is_available}
        self.save_changes()

    def save_borrow(self, borrow: Borrow):
        self.data['borrow_data'][borrow.book_title][borrow.borrowed_by] = {'user_status': borrow.user_status,
                                                                            'borrowed_on': borrow.borrowed_on,
                                                                            'borrow_deadline': borrow.borrow_deadline,
                                                                            'returned_on': borrow.returned_on}
        self.save_changes()





class Update(GeneralDataHandling):
    def __init__(self, file='data/storage.json'):
        super().__init__(file)

    # This only works for accounts, authors, and books. Borrow has a specific dataset structure.
    def update_entry(self, valid_dataset: list[str]):
        dataset, name, field, new_value = valid_dataset
        accepted_datasets = ['accounts', 'authors', 'library']

        # I dont think this is necessary, but just in case...
        if dataset not in accepted_datasets:
            return
        
        # Saves the updated info to whichever dataset (only for accounts, authors, and library) you changed.
        for valid_dataset in accepted_datasets:
            if dataset == valid_dataset:
                self.data[dataset][name][field] = new_value
        self.save_changes()
    
    def update_borrow(self, data: list[str]):
        book_title, borrower, field, new_value = data
        self.data['borrows'][book_title][borrower][field] = new_value
        self.save_changes()
        



class Delete(GeneralDataHandling):
    def __init__(self, file='data/storage.json'):
        super().__init__(file)

    # Again, this follows the same logic as with update, wherein this only works for accounts, authors, and library.
    def delete_entry(self, dataset: str, name: str):
        accepted_datasets = ['accounts', 'authors', 'library']

        for valid_dataset in accepted_datasets:
            if dataset == valid_dataset:
                self.data[dataset].pop(name)
        self.save_changes()

    def delete_borrow(self, data: list[str]):
        book_title, borrower = data
        self.data['borrows'][book_title].pop(borrower)
        self.save_changes()