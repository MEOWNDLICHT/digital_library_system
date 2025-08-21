""" Since im stupid af and dont know how to proceed, this is where i will be storing the how-to for the commands. """


general_commands = {
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


system_commands = {
    "stop/end": "Stops the program.",
    "get_current_role": "...",
    "my_info": "..."
}



def about_commands():
    """ Provides the list of commands users can use to navigate the program. """

    commands_list = {"GENERAL COMMANDS": general_commands,
                        "LIBRARIAN-ONLY COMMANDS": librarian_commands,
                        "MEMBER-ONLY COMMANDS": member_commands,
                        "SYSTEM COMMANDS": system_commands}
    

    # displays the commands list
    print('Here are the list of commands that may help you navigate this program.\n')
    for label, commands in commands_list.items():
        print(label)
        for command, description in commands.items():
            print(f"{command}: {description}")
        print()



def about_me():
    """ Provides the personal information of the current user. """
    pass