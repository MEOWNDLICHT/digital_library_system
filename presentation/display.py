""" This is where the CLI-based interactions are supposed to be handled. """

from .acc_verify import login, sign_up
from .actions import actions

class UserInteraction:
    # for aethetic purposes
    linebreak = "\n-----------------------------------------------------------------------------\n"

    def __init__(self):
        self.greet()
        self.how_to_use()   
        self.user_status()
        
        try:
            while True:
                print(self.linebreak)
                user_action = str(input("What do you want to do? -> ")).strip()
                actions(user_action, self.user_access)
        
        except AttributeError:
            print(f'\nAccess Denied. User tried to access a command beyond their role.')
            print(f'Access limited to {self.user_access}.')

        except Exception as e:
            print(f"ERROR: {e}")


    def user_status(self):
        """ Ask the user whether they are new to the program or not. Directs them to sign_up or login. """
        while True:
            print(self.linebreak)
            status = str(input("Are you new?(y/n) -> ")).strip()

            # does nothing if 'n'.
            if status.lower() == 'n':
                pass 
            elif status.lower() == 'y':
                sign_up()
            else:
                # skip the iteration and start over again.
                print(f"\nInvalid answer: {status}. Can't determine user's status.\n")
                continue 
            
            # prompts the user to login.
            self.user_access = login()
            break


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


    def help(self):
        """ Provides the list of commands users can use to navigate the program. """
        self.general_commands = {
            "search": "Let's you lookup more info about a specific user, book, or author.", 
            "is_available": "Let's you see if a book is currently available for borrow.",
            "user_borrow_history": "Lets's you see the list of books borrowed by the specified user.",
            "book_borrow_history": "Let's you see the list of users who are currently borrowing a specific book.",
            "get_written_books": "Let's you see all the books written by the specified author.",
            "user_metrics": "Let's you see all the users currently registered in the database.",
            "book_metrics": "Let's you see all the books in the library."
            }


        self.librarian_commands = {
            "add_user": "For registering new users into the program.",
            "add_book": "For adding new books to the library.",
            "update_user": "For updating the details of the specified user. Can only update information one at a time.",
            "update_book": "For updating the details of the specified book. Can only update information one at a time.",
            "update_author": "For updating the details of the specified author. Can only update information one at a time.",
            "update_borrow": "For updating the details of the specified borrow information. Can only update information one at a time.",
            "remove_user": "For removing a specific user from the program.",
            "remove_book": "For removing a book from the library."
        }


        self.member_commands = {
            "borrow_book": "Let's the user borrow a book from the library if available. Return deadline is two weeks.",
            "return_book": "Let's the user return a book they have borrowed back to the library."
        }

        self.system_commands = {
            "stop/end": "Stops the program.",
            "...": "..."
        }

        commands_list = {"GENERAL COMMANDS": self.general_commands,
                         "LIBRARIAN-ONLY COMMANDS": self.librarian_commands,
                         "MEMBER-ONLY COMMANDS": self.member_commands,
                         "SYSTEM COMMANDS": self.system_commands}
        
        # displays the commands list
        print('Here are the list of commands that may help you navigate this program.\n')
        for label, commands in commands_list.items():
            print(label)
            for command, description in commands.items():
                print(f"{command}: {description}")
            print()

        