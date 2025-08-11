""" This is where the CLI-based interactions are supposed to be handled. """

from .operations import GeneralServices, LibrarianServices, MemberServices
from .error import NameNotFoundError
import os, sys, time, json


class UserInteraction:
    DEFAULT_DATASETS = {'accounts': {}, 
                    'authors': {},
                    'library': {},
                    'borrows': {}}

    def __init__(self):
        self.greet()
        self.how_to_use()
        user_role = self.login()

        # separates user access to different methods based on user's role.
        if user_role == 'librarian':
            service = LibrarianServices()
        elif user_role == 'member':
            service = MemberServices()
        else:
            service = GeneralServices()

        while True:
            activity = str(input("\nWhat do you want to do? -> ")).strip()  
            try:
                match activity:
                    # GENERAL ACCESS COMMAND
                    case 'is_available':
                        pass
                    
                    case 'user_borrow_history':
                        pass
                    
                    case 'book_borrow_history':
                        pass
                    
                    case 'get_written_books':
                        pass
                    
                    case 'user_metrics':
                        pass
                    
                    case 'book_metrics':
                        pass


                    # LIBRARIAN-ONLY COMMANDS
                    case 'add_user':
                        pass

                    case 'add_book':
                        pass

                    case 'update_user':
                        pass

                    case 'update_book':
                        pass

                    case 'update_author':
                        pass

                    case 'update_borrow':
                        pass

                    case 'remove_user':
                        pass

                    case 'remove_book':
                        pass


                    # MEMBER-ONLY COMMANDS
                    case 'borrow_book':
                        pass

                    case 'return_book':
                        pass


                    # MISCELLANEOUS/SYSTEM COMMANDS
                    case ('stop', 'end'):
                        print('Exiting the program. Goodbye!')
                        time.sleep(2)
                        sys.exit()
                    
                    case _:
                        print('Invalid command. Try again.')
            
            except AttributeError:
                print(f'Access Denied. User tried to access a command beyond their role.')
                print(f'Access limited to {user_role}.')


    def login(self, file='data/storage.json'):
        """ Authenticates the user.
            
            Returns:
                attr: the user's role. """
        # checks if the json file exists and sets the default data structures
        if not os.path.exists(file):
            with open(file, "w") as create_file:
                json.dump(self.DEFAULT_DATASETS, create_file, indent=4)

        try:
            with open(file, "r") as f:
                self.data = json.load(f)

        # to ensure that the program wouldn't break regardless of whether storage.json is empty or cannot be found.
        except (json.JSONDecodeError, FileNotFoundError):
            self.data = self.DEFAULT_DATASETS.copy()

        user_name = str(input("\nEnter your username -> ")).strip()
        self.accounts = self.data['accounts']

        if user_name not in self.accounts:
            raise NameNotFoundError(username=user_name)
        else:
            return self.accounts[user_name].get("role")



    def greet(self):
        """ Greets the users who are using the program. """
        print("\nWelcome, user!")
        print("This is a program that simulates digital library systems through CLI.")
        print("This piece of shit program may or may not run well.")
        print("Don't expect too much.")


    def how_to_use(self):
        """ Provides the basic how-to for using the program. """
        print("\n\nHOW TO USE:")
        print("1. Type 'stop' or 'end' to stop the program.")
        print("2. Type 'help' to get the list of commands you can use to navigate the program.")
        print("3. If something breaks, don't worry, it's normal. I ain't fixing it tho.")


    def list_of_services(self):
        """ Provides the list of commands users can use to navigate the program. """
        general_comamnds = {
            "search": "Let's you lookup more info about a specific user, book, or author.", 
            "is_available": "Let's you see if a book is currently available for borrow.",
            "user_borrow_history": "Lets's you see the list of books borrowed by the specified user.",
            "book_borrow_history": "Let's you see the list of users who are currently borrowing a specific book.",
            "get_written_books": "Let's you see all the books written by the specified author.",
            "user_metrics": "Let's you see all the users currently registered in the database.",
            "book_metrics": "Let's you see all the books in the library."
            }


        librarian_commands = {
            "add_user": "For registering new users into the program.",
            "add_book": "For adding new books to the library.",
            "update_user": "For updating the details of the specified user. Can only update information one at a time.",
            "update_book": "For updating the details of the specified book. Can only update information one at a time.",
            "update_author": "For updating the details of the specified author. Can only update information one at a time.",
            "update_borrow": "For updating the details of the specified borrow information. Can only update information one at a time.",
            "remove_user": "For removing a specific user from the program.",
            "remove_book": "For removing a book from the library."
        }


        member_commands = {
            "borrow_book": "Let's the user borrow a book from the library if available. Return deadline is two weeks.",
            "return_book": "Let's the user return a book they have borrowed back to the library."
        }