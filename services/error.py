""" This is where checks and errors are handled. """


class Error(Exception):
    pass

class EmptyValueError(Error):
    """ Raised if empty values were detected among the arguments. """
    def __init__(self):
        super().__init__('Empty values detected.')
    
class NameTakenError(Error):
    """ Raised if name of type User, Author, or Book is already taken.  """

class NameNotFoundError(Error):
    """ Raised if name of type User, Author, or Book cannot be found in the database. """

class InvalidAgeError(Error):
    """ Raised if age entered is lower (<13) or greater (>150) than the valid age limit. """
    def __init__(self):
        super().__init__('Invalid age entered.')

class InvalidEmailError(Error):
    """ Raised if email entered is invalid. """
    def __init__(self):
        super().__init__('Must only be either in Gmail ("@gmail.com") or Yahoo ("@yahoo.com").')

class InvalidChangeError(Error):
    """ Raised if a sensitive field and field value had been attempted to change. """