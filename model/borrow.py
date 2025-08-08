""" Here is the blueprint for the borrow informations object """

class Borrow:
    def __init__(self, book_title: str, borrowed_by: str, borrowed_on: str, borrow_deadline: str, returned_on='unknown', user_status='active'):
        self.book_title = book_title
        self.borrowed_by = borrowed_by
        self.borrowed_on = borrowed_on
        self.borrow_deadline = borrow_deadline
        self.returned_on = returned_on
        self.user_status = user_status