""" FOR USER RELATED AUTHENTICATION. """

from services import LibrarianServices, NameNotFoundError
import os, json

DEFAULT_DATASETS = {'accounts': {}, 
                'authors': {},
                'library': {},
                'borrows': {}}


def login(file='data/storage.json'):
    """ Authenticates the user if they already have an existing account.
        
        Returns:
            attr: the user's role. """
    # checks if the json file exists and sets the default data structures
    if not os.path.exists(file):
        with open(file, "w") as create_file:
            json.dump(DEFAULT_DATASETS, create_file, indent=4)

    try:
        with open(file, "r") as f:
            data = json.load(f)

    # to ensure that the program wouldn't break regardless of whether storage.json is empty or cannot be found.
    except (json.JSONDecodeError, FileNotFoundError):
        data = DEFAULT_DATASETS.copy()

    user_name = str(input("\nEnter your username -> ")).strip()
    accounts = data['accounts']

    if user_name not in accounts:
        raise NameNotFoundError(username=user_name)
    else:
        return accounts[user_name].get("role")
    

def sign_up():
    """ Registers a new user into the database. Calls login after user creation is successful. """
    temporary_librarian_access = LibrarianServices()
    while True:
        try:
            username = input('Enter your desired username here -> ').strip()
            email = input('Enter your email address here -> ').strip()
            age = int(input('Enter your current age here -> '))

            # creates the account.
            temporary_librarian_access.add_user(username, email, age)
            print('Account successfully created! Directing user to login now...')

        # tbc
        except Exception:
            pass