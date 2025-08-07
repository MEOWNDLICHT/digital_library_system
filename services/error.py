""" This is where custom errors are handled. """


class Error(Exception):
    pass


class EmptyValueError(Error):
    """ Raised if empty values were detected among the arguments. """
    def __init__(self):
        super().__init__('Empty values detected.')
    

class NameTakenError(Error):
    """ Raised if name of type User, Author, or Book is already taken.  """
    def __init__(self, name: str):
        super().__init__(f"'{name}' already taken!")


class NameNotFoundError(Error):
    """ Raised if name of type User, Author, or Book cannot be found in the database. """
    def __init__(self, entity_type: str, name: str):
        super().__init__(f"{entity_type.capitalize()}, '{name}', cannot be found!")


class InvalidAgeError(Error):
    """ Raised if age entered is lower (<13) or greater (>150) than the valid age limit. """
    def __init__(self):
        super().__init__('Invalid age entered.')


class InvalidEmailError(Error):
    """ Raised if email entered is invalid. """
    def __init__(self):
        super().__init__('Must only be either in Gmail ("@gmail.com") or Yahoo ("@yahoo.com").')


class InvalidChangeError(Error):
    """ Raised if a sensitive data has been tried to change. """
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
    def __init__(self, error_type: str):
        if error_type == 'quantity_not_int':
            message = 'Book quantity must only be expressed in natural numbers.'
        elif error_type == 'quantity_less_than_zero':
            message = 'Book quantity must not be less than zero.'
        else:
            message = 'Quantity invalid.'
        super().__init__(message)