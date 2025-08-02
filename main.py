""" This should be the only place where you should run the code, otherside it may behave unexpectedly. """

from data import AccountsData, LibraryData, AuthorsData, BorrowData
from services import GeneralServices, LibrarianServices, MemberServices



def run_packages():
    library = LibrarianServices()
    library.create_user('SampleUser1', 'sampleuser1@gmail.com', 25)

    




if __name__ == '__main__':
    run_packages()  