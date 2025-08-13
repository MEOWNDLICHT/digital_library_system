""" Here is the blueprint for the author object """

class Author:
    def __init__(self, name: str, age='unknown', birthday='unknown', nationality='unknown', books=[]):
        self.name = name
        self.age = age
        self.birthday = birthday
        self.nationality = nationality
        self.books = books