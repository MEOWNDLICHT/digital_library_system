""" Handles user actions when prompted what to do. """

from services import LibrarianServices, MemberServices
from .help import help
from services.error import EmptyValueError, NameNotFoundError, NameTakenError, InvalidAgeError, InvalidChangeError, InvalidEmailError, InvalidQuantityError, BookUnavailableError
import sys, time


def action(action, access):
     # for aethetic purposes
    linebreak = "\n-----------------------------------------------------------------------------\n"

    # separates user access to different methods based on user's role.
    if access == 'librarian':
        service = LibrarianServices()
    elif access == 'member':
        service = MemberServices()

    try:
        match action:
            # GENERAL ACCESS COMMAND
                case 'is_available':
                    print("'is_available' lets you know the book's availability for borrow. BOOK TITLE is required.")
                    book_title = ask_for('book_title')
                    service.is_available(book_title)
                
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
                case 'stop' | 'end':
                    print('\nExiting the program. Goodbye!')
                    time.sleep(2)
                    sys.exit()

                case 'help':
                    help()
                
                case _:
                    print('\nInvalid command. Try again.\n')
    
    except (EmptyValueError, NameNotFoundError, NameTakenError, InvalidAgeError, InvalidChangeError, InvalidEmailError, InvalidQuantityError, BookUnavailableError, ValueError) as e:
        print(f"ERROR: {e}")



def ask_for(object: str):
    """ Ask the user to enter a specific information.
        
        Returns:
            str: The user's answer.  """
    info = input(f"Enter the {object} here -> ")
    return info