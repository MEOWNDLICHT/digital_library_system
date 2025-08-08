""" This is where data is handled for different CRUD operations. All info are stored in json file. """

from model import User, Book, Author, Borrow
import json



class GeneralDataHandling():
    def __init__(self, data, file):
        self.file = file

        if data is not None:
            self.data = data


    def save_changes(self):
        with open(self.file, 'w') as save:
            json.dump(self.data, save, indent=4)
        




class Create(GeneralDataHandling):
    def __init__(self, data, file):
        super().__init__(data, file)

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

    def save_borrow(self, borrow_info: Borrow):
        self.data['borrows'][borrow_info.book_title][borrow_info.borrowed_by] = {'borrowed_on': borrow_info.borrowed_on,
                                                                                'borrow_deadline': borrow_info.borrow_deadline,
                                                                                'returned_on': borrow_info.returned_on,
                                                                                'user_status': borrow_info.user_status}
        self.save_changes()





class Update(GeneralDataHandling):
    def __init__(self, data, file):
        super().__init__(data, file)

    # This only works for accounts, authors, and books. Borrow has a specific dataset structure.
    def update_entry(self, change: list[str]):
        dataset, name, field, new_value = change
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
    def __init__(self, data, file):
        super().__init__(data, file)

    # Again, this follows the same logic as with update, wherein this only works for accounts, authors, and library.
    def delete_entry(self, entry: list[str]):
        dataset, name = entry
        accepted_datasets = ['accounts', 'authors', 'library']

        for valid_dataset in accepted_datasets:
            if dataset == valid_dataset:
                self.data[dataset].pop(name)
        self.save_changes()

    def delete_borrow(self, data: list[str]):
        book_title, borrower = data
        self.data['borrows'][book_title].pop(borrower)
        self.save_changes()