# Library-Management-System
Senior Project Spring 2023

## Problem Description
As I spent most of my time at the library I have been amazed at how many books there are. I realized that there is a lot of data/books that have to be handled, it is necessary to know the books that are checked out, the books that are checked in and the new books that are getting into the library. Without a management system librarians have a hard time with data inconsistency, books are lost, and there is no organization. This problem not only affects the libraries but people that love books and have their own mini libraries at home.

## Solution Description
To solve this problem I created an easy to use library management system a webpage that keeps track of books that are available in the library, books that are checked out and a fast way to add a new book into the library. 

## Technical Overview
In order for the librarian to add a new book to the library database easily, without having to manually add every detail of the book into the database, the librarian has quick access to books and their information from the Google Books API. I connected my JavaScript to the Google Books API so any type of book data (name, author, isbn, or publisher) is used to retrieve a book or books from the API through AJAX and are displayed in the website HTML, by clicking the Add Book to Library button the information from that book is sent to the local API server in Python by using the Fetch() method and then added to the SQlite database. 
The library database contains two tables, one contains the books available in the library and the other table contains the books that are checked out. The database and its tables are integrated and handled in SQlite through Python.
The books in the library and books checked out and their information are displayed in the HTML website by Fetch API accessing requests and responses between the database and the website through JavaScript and passed to HTML. To check in or check out a book its data is passed by the server API and its information is moved (deleted and added) between the database tables.
