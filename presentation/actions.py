""" Handles user actions when prompted what to do. """

from services import LibrarianServices, MemberServices
from .help import about_commands
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
        print(f"\nProceeding with {action}...\n")
        match action.lower():
            # GENERAL ACCESS COMMAND
                case 'is_available':
                    book_title = ask_for("book's title")
                    service.is_available(book_title)


                case 'search':
                    what_to_search = input('What do you want to search for? -> ')
                    
                    if what_to_search.lower() not in ['user', 'book', 'author']:
                        print('\nSearch invalid. Can only search for user, book, and author.')
                        return 
        
                    name = ask_for(what_to_search.lower())
                    service.search(what_to_search, name)


                case 'user_borrow_history':
                    username = ask_for('username')
                    service.user_borrow_history(username)


                case 'book_borrow_history':
                    book_title = ask_for("book's title")
                    service.book_borrow_history(book_title)


                case 'get_written_books':
                    username = ask_for('username')
                    service.get_written_books(username)


                case 'user_metrics':
                    service.user_metrics()


                case 'book_metrics':
                    service.book_metrics()



                # LIBRARIAN-ONLY COMMANDS
                case 'add_user':
                    username = ask_for('username')
                    email = ask_for('email')
                    age = ask_for('age')
                    service.add_user(username, email, age)
                    print(f"User, '{username}', has been added to the database!")


                case 'add_book':
                    book_title = ask_for("book's title")
                    author = ask_for('author')
                    quantity = ask_for("book's quantity")
                    ask_further_info = input('\nDo you want to continue adding more info? -> (y/n)') 
                    
                    if ask_further_info == 'y':
                        publishing_date = ask_for('publishing date')
                        book_genre = ask_for('genre')
                        restriction = ask_for('age rating')
                        service.add_book(book_title, author, quantity, publishing_date, book_genre, restriction)
                        print(f"Book, '{book_title}', has been added to the database!")
                        return
                    
                    service.add_book(book_title, author, quantity)
                    print(f"Book, '{book_title}', has been added to the database!")


                case 'update_user':
                    username = ask_for('username')
                    field = ask_for('field name')
                    new_value = ask_for('new value')
                    service.update_user(username, field, new_value)
                    print(f"User's information has been updated!")


                case 'update_book':
                    book_title = ask_for("book's title")
                    field = ask_for('field name')
                    new_value = ask_for('new value')
                    service.update_book(book_title, field, new_value)
                    print(f"Book's information has been updated!")


                case 'update_author':
                    author = ask_for("author's name")
                    field = ask_for('field name')
                    new_value = ask_for('new value')
                    service.update_user(author, field, new_value)
                    print(f"Author's information has been updated!")


                case 'update_borrow':
                    book_title = ask_for("book's title")
                    username = ask_for('username')
                    field = ask_for('field name')
                    new_value = ask_for('new value')
                    service.update_user(book_title, username, field, new_value)
                    print(f"User's borrow information has been updated!")


                case 'remove_user':
                    username = ask_for('username')
                    service.remove_user(username)
                    print(f"User, {username}, has been removed!")


                case 'remove_book':
                    book_title = ask_for("book's title")
                    service.remove_user(book_title)
                    print(f"Book, {book_title}, has been removed!")



                # MEMBER-ONLY COMMANDS
                case 'borrow_book':
                    book_title = ask_for("book's title")
                    borrower = ask_for("borrower's name")
                    service.borrow_book(book_title, borrower)
                    print(f"Book, {book_title}, has been successfuly borrowed!")
                    print('Note that you must return the book within two weeks, or you may be penalized.')
                    print('Enjoy reading!')



                case 'return_book':
                    book_title = ask_for("book's title")
                    borrower = ask_for("borrower's name")
                    service.borrow_book(book_title, borrower)
                    print(f"Book, {book_title}, has been successfuly returned!")
                    print('Thank you for reading!')



                # MISCELLANEOUS/SYSTEM COMMANDS
                case 'stop' | 'end':
                    print('\nExiting the program. Goodbye!')
                    time.sleep(2)
                    sys.exit()


                case 'help':
                    about_commands()


                case _:
                    print('\nInvalid command. Try again.')


    except (EmptyValueError, NameNotFoundError, NameTakenError, InvalidAgeError, InvalidChangeError, InvalidEmailError, InvalidQuantityError, BookUnavailableError, ValueError) as e:
        print(f"ERROR: {e}")



def ask_for(object: str):
    """ Ask the user to enter a specific information.
        
        Returns:
            str: The user's answer.  """
    if object == 'age':
        info = int(input(f"Enter the age here -> "))
    else:
        info = input(f"Enter the {object} here -> ")
    return info