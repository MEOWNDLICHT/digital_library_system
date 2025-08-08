""" Where validation and checks are handled. """



class Check():
    def __init__(self, data, file):
        self.file = file

        if data is not None:
            self.data = data

        # Shorthands to ease each dataset calls
        self.accounts = self.data['accounts']
        self.library = self.data['library']
        self.authors = self.data['authors']
        self.borrow_booklist = self.data['borrows'].keys()
        self.borrow_userlist = [user for users in self.data['borrows'].values() for user in users]


    @staticmethod
    def detect_empty_values(*args: str):
        """ Checks to see if there are any empty values detected in the input.
            
            Returns:
                bool: True if any empty input values are detected, otherwise False. """
        if not any(str(value).strip() for value in args):
            return True
        return False


    @staticmethod
    def is_valid(name='unknown', email='sample@gmail.com', role='member', age=18, quantity=1, is_available=True):
        """ Checks if a value that the user has given is valid
            
            Returns:
                bool: True if valid, False otherwise. """
        # checks if the arg is accurate to the data type needed
        if not isinstance(name, str):
            return False
        if not isinstance(age, int):
            return False
        if not isinstance(email, str):
            return False
        if not isinstance(role, str):
            return False
        if not isinstance(quantity, int):
            return False
        if not isinstance(is_available, bool):
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
    
    

    # NOTE: Don't forget to specify the parameter name before entering the value u want to check (username = name_of_user).
    def exists(self, username=None, book_title=None, author_name=None, borrow_bookname=None, borrow_username=None, field=None):
        """ Checks for the existence of an item in the dataset.  
            
            Returns:
                bool: True if item found (or it exists), otherwise False. """
        if username in self.accounts:
            return True
        if book_title in self.library:
            return True
        if author_name in self.authors:
            return True
        if borrow_bookname in self.borrow_booklist:
            return True
        if borrow_username in self.borrow_userlist:
            return True
        
        # This only works for the first three datasets: accounts, library, and authors
        for dataset in self.data.values():
            for names in dataset.values():
                if field in names.keys():
                    return True

        # borrow dataset has a very specific structure
        for title in self.borrow:
            for borrowers in self.borrow[title]:
                if field in self.borrow[title][borrowers].keys():
                    return True
        return False
    
