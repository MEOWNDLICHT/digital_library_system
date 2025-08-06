""" Where validation and checks are handled. """



class Check():
    def __init__(self):
        ...
        

    """Checks to see if there are any empty values detected in the input.
        RETURNS:
            bool: True if any empty input values are detected, otherwise False. """
    @staticmethod
    def detect_empty_values(*args: str):
        if any(str(value).strip() for value in args):
            return True
        return False


    """ Checks if a value that the user has given is valid
        RETURN:
            bool: True if valid, False otherwise. """
    @staticmethod
    def is_valid(name='unknown', email='sample@gmail.com', role='member', age=18):
        # checks if the arg is accurate to the data type needed
        if not isinstance(name, str):
            return False
        if not isinstance(age, int):
            return False
        if not isinstance(email, str):
            return False
        if not isinstance(role, str):
            return False
        
        # age validation
        if age < 13 or age > 120:
            return False
        
        # email validation
        if '@' not in email:
            return False
        elif email.split('@')[1].lower() not in ['gmail.com', 'yahoo.com']:
            return False
        
        # role validation
        if role.lower() not in ['librarian', 'member']:
            return False
        return True


    """ Checks for the existence of an item in the dataset.   
    RETURNS:
        bool: True if item found (or it exists), otherwise False. """
    def exists(self):
        ...