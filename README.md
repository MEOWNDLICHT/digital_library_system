# Digital Library System

A CLI-based simulation of digital library system that supports basic CRUD operations for managing books, users, authors, and borrowing information. Users are authenticated and given access to varying operations based on their role (librarian/member). Everything about this program is made unnecessarily complex. This has no real value other than for educational purposes.   

---

## Roles and Access  
### General  
- Can see if a book is available for borrow  
- Can know more details regarding the book or a user's borrow history
- Can access information and know more details regarding a user, book or author  
- Can get a list of books that an author has written  
- Can get metrics related to the total number of books and users in the program  

### Members  
- Can borrow and return books.  

### Librarians
- Can create, delete, update user accounts and information  
- Can add, remove, update book informations  
- Can update author-related informations  
- Can update borrow-related information  

---

## How Does It Work?  

IDK yet.  
Still a WIP. I kind of want to abandon this sht.  
The service layer is giving me a headache.  
Some methods work, but spaghetti code is lurking. Needs cleanup.  

---

## Project Structure / Flow  
#### main.py -> presentaion -> services -> data -> model  


main.py - starting point  
presentation - handles the CLI-interactions and display  
services - where the CRUD operations are properly handled and authenticated  
data - where data is stored and updated  
model - where the basic blueprints for accounts, users, and such are handled  

---

## Project Status  

This project is almost done.  
Just need to test everything and it should work relatively okayish.  
It might still break if you deliberately try to do it. But overall it should be fine.  
I don't wanna continue this anymore.  

---

### GOODNIGHT~
