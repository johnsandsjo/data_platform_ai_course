from fastapi import FastAPI, Query
from data_processing import library_data
from data_processing import Book
from pprint import pprint
from constants import CURRENT_YEAR, DATA_PATH
import json

library = library_data("library.json")
books = library.books

app=FastAPI()

@app.get("/books")
async def read_books():
    return books

#path parameter
@app.get("/books/title/{title}")
async def read_book_by_title(title: str):
    return [book for book in books if book.title.casefold() == title.casefold()]

# query parameter - ? after the endpoint
@app.get("/books/")
async def filter_books(
    start_year  : int = Query(
        1950,
        gt = 1500,
        lt = CURRENT_YEAR +1,
        description = "Filters books that are newer than this year"
        ),
        author: str = Query(None, description = "Filter by authors firstname and lastname")
    ):
    filtered_books = [book for book in books if start_year < book.publication_year]
    if author:
        filtered_books = [book for book in filtered_books if author.casefold() == book.author.casefold()]
    
    return filtered_books

@app.post("/books/create_book")
async def create_book(book_request : Book):
    new_book = Book.model_validate(book_request)
    books.append(new_book)
    new_book_dict = book_request.model_dump()
    with open(DATA_PATH / "library.json", "r") as file:
        existing_file = json.load(file)
    
    existing_file["books"].append(new_book_dict)
    
    with open(DATA_PATH / "library.json", "w") as file:
        json.dump(existing_file, file, indent=4)
        
    return new_book

@app.put("/books/update_book")
async def update_book(updated_book: Book):
    for i, book in enumerate(books):
        if book.id == updated_book.id:
            books[i] = updated_book
    with open(DATA_PATH / "library.json", "r") as file:
        current_file = json.load(file)
        for i, book in enumerate(existing_file["books"]):
            if book["id"] == updated_book.id:
                current_file["books"][i] = updated_book.model_dump()
    with open(DATA_PATH / "library.json", "w") as file:
        json.dump(current_file, file, indent=4)
    return updated_book

@app.delete("/books/delete_book/{id}")
async def delete_book(id : int):
    for i, book in enumerate(books):
        if book.id == id:
            del books[i]
            break
    with open(DATA_PATH / "library.json", "r") as file:
        current_file = json.load(file)
        for i, book in enumerate(current_file["books"]):
            if book["id"] == id:
                del current_file["books"][i]
                break
    with open(DATA_PATH / "library.json", "w") as file:
        json.dump(current_file, file, indent=4)