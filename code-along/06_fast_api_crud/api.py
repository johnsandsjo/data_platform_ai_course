from fastapi import FastAPI
from data_processing import library_data, Book

library = library_data("library.json")
books: list[Book] = library.books

app= FastAPI()


@app.get("/books")
async def read_books():
    return books

# books is a list of book

#path parameter
@app.get("/books/book/{id}")
async def read_book_by_id(id: int):
    return [book for book in books if book.id == id]


@app.post("/books/create_book")
async def create_book(book_request: Book):
    new_book = Book.model_validate(book_request)
    books.append(new_book) 
    #detta är en naiv approach för sessionen. Icke persistant. 
    # Annars kan man göra detta med with och open.
    # eller insert into databas - ännu bättre
    return new_book


@app.put("/books/update_book")
async def update_book(updated_book: Book):
    # enumerate plockar ut bok för bok och tar ut index
    for i, book in enumerate(books):
        if book.id == updated_book.id:
            books[i] = updated_book
    return updated_book

@app.delete("/books/delete_book/{id}")
async def update_book(id: int):
    for i, book in enumerate(books):
        if book.id == id:
            del books[i]
            break