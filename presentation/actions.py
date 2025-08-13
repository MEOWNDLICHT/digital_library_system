""" Handles user actions when prompted what to do. """

from services import LibrarianServices, MemberServices
import sys, time


def actions(self, user_action, user_access):
     # for aethetic purposes
    linebreak = "\n-----------------------------------------------------------------------------\n"

    # separates user access to different methods based on user's role.
    if user_access == 'librarian':
        service = LibrarianServices()
    elif user_access == 'member':
        service = MemberServices()


    match user_action:
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
        case 'stop' | 'end':
            print('\nExiting the program. Goodbye!')
            time.sleep(2)
            sys.exit()

        case 'help':
            self.help()
        
        case _:
            print('\nInvalid command. Try again.\n')

