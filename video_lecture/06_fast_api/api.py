from fastapi import FastAPI, Query
from data_processing import library_data
from pprint import pprint
from constants import CURRENT_YEAR

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

# query parameter - ? after the end endpoint
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