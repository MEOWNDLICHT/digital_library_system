""" This is where the CLI-based interactions are supposed to be handled. """

from .acc_verify import login, sign_up
from .actions import action


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
                action(user_action, self.user_access)
        
        except AttributeError:
            print(f'\nAccess Denied. User tried to access a command beyond their role.')
            print(f'Access limited to {self.user_access}.')

        # except Exception as e:
        #     print(f"ERROR: {e}")



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