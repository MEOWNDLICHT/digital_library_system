from model import Author

class Book:
    # For tracking total number of books
    total_number = 0

    def __init__(self, title: str, author: str, quantity: int, date_published='Unknown', genre='Unknown', age_restriction='all-ages', is_available=True):
        self.title = title
        self.author = author
        self.quantity = quantity
        self.date_published = date_published
        self.genre = genre
        self.age_restriction = age_restriction
        self.is_available = is_available
