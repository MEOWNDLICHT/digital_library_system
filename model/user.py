class User:
    def __init__(self, username: str, email: str, age: int, id: str, role='Member', remaining_borrow=10, borrow_limit=10, borrowed_books=[]):
        self.username = username
        self.email = email
        self.age = age
        self.id = id
        self.role = role
        self.remaining_borrow = remaining_borrow
        self.borrow_limit = borrow_limit
        self.borrowed_books = borrowed_books


    def __repr__(self):
        return f"REPR: User(username='{self.username}', email='{self.email}', age='{self.age}', id='{self.id}', role='{self.role}')"
    
    def __str__(self):
        return f"STR: username='{self.username}', email='{self.email}', age='{self.age}', id='{self.id}', role='{self.role}'"