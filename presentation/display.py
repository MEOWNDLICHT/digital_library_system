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
        
        # checks if user has successfuly log-on
        if self.login_status is not None: 
            # asks the user for action or command
            while True:
                try:
                        print(self.linebreak)
                        user_action = str(input("What do you want to do? -> ")).strip()
                        print()
                        action(user_action, self.login_status)
                
                except AttributeError:
                    print(f'\nACCESS DENIED.\nUser tried to access a command beyond their role.')
                    print(f'Access limited to {self.login_status[0]}.')
        else:
            # if unsuccessful, returns to login/sign-up status
            print('\nMaximum login attempt reached. Returning to start.\n')
            self.user_status()


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
                print(f"\nInvalid answer: '{status}'. Can't determine user's status.\n")
                continue 
            
            # prompts the user to login.
            self.login_status = login()
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