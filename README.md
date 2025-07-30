# Library Simulation Program  
### Created by: Meow  

A CLI-based simulation of digital library system that supports basic CRUD operations for managing books, users, authors, and borrowing information, including a two-way user authentication and role-based (librarian/member) access control to differentiate between user permissions.  

---

## How Does It Work?  

Honestly? IDK yet.  
Still a WIP. I kind of want to abandon this sht.  
The service layer is giving me a headache.  
Some methods work, but spaghetti code is lurking. Needs cleanup.  

---

## Project Structure / Flow  
main.py -> services -> data -> model


main.py - handles the proper execution of everything  
services - where the CRUD operations are properly handled and authenticated  
data - where data is stored and updated  
model - where the basic blueprints for accounts, users, and such are handled  


### GOODNIGHT~