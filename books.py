import json
from urllib.request import urlopen


#TEST

def find_book_by_ISBN():
    
    API_URL = "https://www.googleapis.com/books/v1/volumes?q=inauthor:Richard+Moreno"

    response = urlopen(API_URL)

    book_data = json.load(response)

    print(book_data)

    
find_book_by_ISBN()