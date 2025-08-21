""" FOR USER RELATED AUTHENTICATION. """

from services import LibrarianServices, EmptyValueError, NameNotFoundError, NameTakenError, InvalidAgeError, InvalidEmailError
import os, json


# for setting default datasets structure in the json
DEFAULT_DATASETS = {'accounts': {}, 
                'authors': {},
                'library': {},
                'borrows': {}}

# for aethetic purposes; used in making the presentation flow easier to understand.
linebreak = "\n-----------------------------------------------------------------------------\n"


def login(file='data/storage.json'):
    """ Authenticates the user if they already have an existing account.
        
        Returns:
            attr: the user's role and name. """
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

    accounts = data['accounts']
    # loops until the user has logged into an account stored in the database.
    login_attempt = 0
    while True:
        print(linebreak)
        print('LOGIN')
        user_name = str(input("Enter your username -> ")).strip()
        login_attempt += 1

        if login_attempt > 5:
            return

        try:
            if user_name not in accounts:
                raise NameNotFoundError(username=user_name)
            else:
                user_role = accounts[user_name].get("role")
                print("\nLogin Successful!")
                print(f"Welcome back, {user_name}!")
                return [user_role, user_name]
        except NameNotFoundError as e:
            print(f'\nERROR: {e}')
    

def sign_up():
    """ Registers a new user into the database. Calls login after user creation is successful. """
    temporary_librarian_access = LibrarianServices()
    while True:
        try:
            print(linebreak)
            print('SIGN-UP')
            username = input('Enter your desired username here -> ').strip()
            email = input('Enter your email address here -> ').strip()
            age = int(input('Enter your current age here -> '))

            # creates the account.
            temporary_librarian_access.add_user(username, email, age)
            print('\nAccount successfully created!\nDirecting user to login now...')
            break

        except (EmptyValueError, NameTakenError, InvalidAgeError, InvalidEmailError) as e:
            print(f"\nERROR: {e}")

        except Exception:
            print("\nSomething went wrong!")