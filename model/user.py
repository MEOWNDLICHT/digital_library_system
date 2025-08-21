""" Here is the blueprint for the user object """

class User:
    def __init__(self, username: str, email: str, age: int, id: str, role='member',borrow_count=0, borrowed_books=[]):
        self.username = username
        self.email = email
        self.age = age
        self.id = id
        self.role = role
        self.borrow_count = borrow_count
        self.borrowed_books = borrowed_books or []
