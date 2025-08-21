""" This is where custom errors are handled. """


class Error(Exception):
    pass


class EmptyValueError(Error):
    """ Raised when empty values are detected among the arguments. """
    def __init__(self):
        super().__init__('Empty values detected.')
    

class NameTakenError(Error):
    """ Raised when name of type user, author, or book is already taken.  """
    def __init__(self, name: str):
        super().__init__(f"'{name}' already taken!")


class NameNotFoundError(Error):
    """ Raised when name of type user, author, or book cannot be found in the database. """
    def __init__(self, username=None, author=None, book_title=None, borrowed_book=None, borrower=None, field=None):
        if username:
            message = f"User, '{username}', cannot be found in the database for 'accounts'!"
        elif author:
            message = f"Author, '{author}', cannot be found in the database for 'authors'!"
        elif book_title:
            message = f"Book, '{book_title}', cannot be found in the database for 'library'!"
        elif borrowed_book:
            message = f"Borrowed book, '{borrowed_book}', cannot be found in the database for 'borrows'!"
        elif borrower:
            message = f"Borrower, '{borrower}', cannot be found in the database for 'borrows'!"
        elif field:
            message = f'Field, {field}, cannot be found!'
        else:
            message = 'Name cannot be found!'
        super().__init__(message)


class InvalidAgeError(Error):
    """ Raised if age entered is lower (<13) or greater (>150) than the valid age limit. """
    def __init__(self):
        super().__init__('Invalid age entered. Must be 12 < age < 150')


class InvalidEmailError(Error):
    """ Raised when email entered is invalid. """
    def __init__(self):
        super().__init__('Must only be either in Gmail ("@gmail.com") or Yahoo ("@yahoo.com").')


class InvalidChangeError(Error):
    """ Raised when a sensitive data has been tried to change. """
    def __init__(self, entity_type: str, name=None, value=None):
        if entity_type == 'field' and name == 'age_restriction':
            message = f"Field, {name}, cannot be change to '{value}'. Must only be 'all-ages'/'mature'."
        elif entity_type == 'field':
            message = f'Field, {name}, cannot be change for security reasons and convenience.'
        elif entity_type == 'role':
            message = "Roles are only limited to 'librarian'/'member'."
        else:
            message = 'An invalid change has been attempted.'
        super.__init__(message)


class InvalidQuantityError(Error):
    """ Raised when the quantity given to a specific object (eg, a book) is invalid or unrealistic. """
    def __init__(self, error_type: str):
        if error_type == 'quantity_not_int':
            message = 'Book quantity must only be expressed in natural numbers.'
        elif error_type == 'quantity_less_than_zero':
            message = 'Book quantity must not be less than zero.'
        else:
            message = 'Quantity invalid.'
        super().__init__(message)


class BookUnavailableError(Error):
    """ Raised when a book is currently unavailable for borrow. """
    def __init__(self, title):
        super().__init__(f"Book, '{title}', is unavailable for borrow.")


class BorrowLimitError(Error):
    """ Raised when the user has exceeded the maximum limit for book borrows. """
    def __init__(self):
        super().__init__("Maximum book borrow limit reached. Can't borrow more books.")