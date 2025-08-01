class Author:
    # For tracking total number of authors
    total_number = 0

    def __init__(self, name: str, age='Unknown', birthday='Unknown', nationality='Unknown', books=[]):
        self.name = name
        self.age = age
        self.birthday = birthday
        self.nationality = nationality
        self.books = books

        