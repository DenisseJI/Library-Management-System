from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from socketserver import ThreadingMixIn
import sqlite3
from sqlite3 import Error
import json

###LOCAL API SERVER###
class MyRequestHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    #GET
    def retrieveBooksLibrary(self):
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.end_headers()

        db = LibraryDatabase()

        books = db.getAllBooksLibrary()

        self.wfile.write(bytes(json.dumps(books), "utf-8"))
        
    #GET
    def retrieveBooksCheckedOut(self):
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.end_headers()

        db = LibraryDatabase()

        books = db.getAllBooksCheckedOut()

        self.wfile.write(bytes(json.dumps(books), "utf-8"))


    #POST
    def addBookLibrary(self):
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body: ", request_body)

        parsed_body = parse_qs(request_body)
        print("Parsed body: ", parsed_body)

        book_title = parsed_body['title'][0]
        book_author = parsed_body['author'][0]
        book_isbn = parsed_body['isbn'][0]
        book_publisher = parsed_body['publisher'][0]
        book_img = parsed_body['img'][0]

        db = LibraryDatabase()

        db.insertBookLibrary(book_title,book_author, book_isbn, book_publisher, book_img, 1)
    
        self.send_response(201)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Added", "utf-8"))

    #POST
    def addBookCheckedOut(self):
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body: ", request_body)

        parsed_body = parse_qs(request_body)
        print("Parsed body: ", parsed_body)

        book_title = parsed_body['title'][0]
        book_author = parsed_body['author'][0]
        book_isbn = parsed_body['isbn'][0]
        book_publisher = parsed_body['publisher'][0]
        book_img = parsed_body['img'][0]

        db = LibraryDatabase()
        db.insertBookCheckedOut(book_title,book_author, book_isbn, book_publisher, book_img, 1)
        db = LibraryDatabase()
        db.deleteBookLibrary(book_isbn)
    
        self.send_response(201)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Added", "utf-8"))

    #POST
    def addBookCheckedIn(self):
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("raw request body: ", request_body)

        parsed_body = parse_qs(request_body)
        print("Parsed body: ", parsed_body)

        book_title = parsed_body['title'][0]
        book_author = parsed_body['author'][0]
        book_isbn = parsed_body['isbn'][0]
        book_publisher = parsed_body['publisher'][0]
        book_img = parsed_body['img'][0]

        db = LibraryDatabase()
        db.insertBookLibrary(book_title,book_author, book_isbn, book_publisher, book_img, 1)
        db = LibraryDatabase()
        db.deleteBookOut(book_isbn)
    
        self.send_response(201)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Added", "utf-8"))


    def do_POST(self):
        print("the post path is: ", self.path)
        if self.path== "/book":
            self.addBookLibrary()
        elif self.path=="/bookout":
            self.addBookCheckedOut()
        elif self.path=="/bookin":
        
            self.addBookCheckedIn()
        else:
            self.handleNotFound()

    
    def do_GET(self):
        print("the request path is: ", self.path)
        if self.path == "/book":
            self.retrieveBooksLibrary()
        elif self.path == "/bookout":
            self.retrieveBooksCheckedOut()
        else:
            self.handleNotFound()

    def handleNotFound(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not found.", "utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods", "GET, POST")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass



FILE = 'library.db'

###### DATABASE #####
class LibraryDatabase:
    def __init__(self) -> None:
        pass

    def createConnection(self):
        connection = None
        try:
            connection = sqlite3.connect(FILE)
        except Error as error:
            print(error)
        
        print("Connected to SQLite")
        print("Database openened successfully")
        return connection

    def createTableLibrary(self):
        connection = self.createConnection()
        connection.execute('''CREATE TABLE IF NOT EXISTS Library
                            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            Title CHAR(255) NOT NULL,
                            Author CHAR(255),
                            ISBN CHAR(255) NOT NULL UNIQUE,
                            Publisher CHAR(255),
                            img_url CHAR(255),
                            Quantity INT)''')
        
        connection.close()
        print("Library Table Created")

    def createTableCheckedOut(self):
        connection = self.createConnection()
        connection.execute('''CREATE TABLE IF NOT EXISTS CheckedOut
                            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            Title CHAR(255) NOT NULL,
                            Author CHAR(255),
                            ISBN CHAR(255) NOT NULL UNIQUE,
                            Publisher CHAR(255),
                            img_url CHAR(255),
                            Quantity INT)''')
        
        connection.close()
        print("CheckedOut Table Created")
        
    def deleteTableLibrary(self):
        try:
            connection = self.createConnection()
            connection.execute('''DROP TABLE Library''')
            connection.commit()
            connection.close()
            print("Library Table Deleted")
        except Error as error:
            print(error)

    def deleteTableCheckedOut(self):
        try:
            connection = self.createConnection()
            connection.execute('''DROP TABLE CheckedOut''')
            connection.commit()
            connection.close()
            print("CheckedOut Table Deleted")
        except Error as error:
            print(error)

    #Title, Author, ISBN, Publisher, img_url, Quantity
        
    def insertBookLibrary(self, title, author, isbn, publisher, img, quantity):

        connection = self.createConnection()
        
        insertion_frase = '''INSERT INTO Library
                            (Title, Author, ISBN, Publisher, img_url, Quantity)
                            VALUES (?, ?, ?, ?, ?, ?)'''
        book_data = (title, author, isbn, publisher, img, quantity)
        

        connection.execute(insertion_frase, book_data)
        connection.commit()
        
        connection.close()

    def insertBookCheckedOut(self, title, author, isbn, publisher, img, quantity):

        connection = self.createConnection()
        
        insertion_frase = '''INSERT INTO CheckedOut
                            (Title, Author, ISBN, Publisher, img_url, Quantity)
                            VALUES (?, ?, ?, ?, ?, ?)'''
        book_data = (title, author, isbn, publisher, img, quantity)
        

        connection.execute(insertion_frase, book_data)
        connection.commit()
        
        connection.close()
        
        
    def showBooksLibrary(self):
        connection = self.createConnection()
        cur = connection.cursor()
        cur.execute('''SELECT * FROM Library''')
        
        rows = cur.fetchall()
        for row in rows:
            print(row)

        cur.close()
    
    
    def getAllBooksLibrary(self):
        connection = self.createConnection()
        cur = connection.cursor()
        cur.execute("SELECT * FROM Library")
        books = cur.fetchall()
        return books
    
    def getAllBooksCheckedOut(self):
        connection = self.createConnection()
        cur = connection.cursor()
        cur.execute("SELECT * FROM CheckedOut")
        books = cur.fetchall()
        return books
        
        
    def getOneBook(self, isbn):
        connection = self.createConnection()
        cur = connection.cursor()
        data = [isbn]
        cur.execute("SELECT * FROM Library WHERE ISBN = ?", data)
        book = cur.fetchone()
        return book
    
    def deleteBookLibrary(self, isbn):
        connection = self.createConnection()
        cur = connection.cursor()
        cur.execute("DELETE FROM Library WHERE ISBN = ?", (isbn,))
        connection.commit()
        
    def deleteBookOut(self, isbn):
        connection = self.createConnection()
        cur = connection.cursor()
        cur.execute("DELETE FROM CheckedOut WHERE ISBN = ?", (isbn,))
        connection.commit()

                          

def run():
    listen = ("127.0.0.1", 8080)
    server = ThreadedHTTPServer(listen,MyRequestHandler)
    #start the server
    print("The server is running!")
    server.serve_forever()

run()



# --manual testing--
#isbn = 1465464530
#db = LibraryDatabase()
#db.deleteBookLibrary(isbn)
#db.insertBook('Harry', 'Senor', 'publisher', '9780747532743', 'url', 1)
#db.createTable()
#db.deleteTable()
#db.showBooksLibrary()
#print(db.getAllBooks())
#print(db.getOneBook('1'))
#db.createTableCheckedOut()

