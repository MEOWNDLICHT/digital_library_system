class Author:
    def __init__(self, name: str, age='Unknown', birthday='Unknown', nationality='Unknown', books=[]):
        self.name = name
        self.age = age
        self.birthday = birthday
        self.nationality = nationality
        self.books = books