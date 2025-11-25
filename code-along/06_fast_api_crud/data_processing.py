from constants import DATA_PATH
import json
from pydantic import BaseModel, Field

def read_json(filename: str):
    with open(DATA_PATH / filename, 'r') as file:
        data = json.load(file)
    
    return data


class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int = Field(gt=1000, lt = 2026, description="Year of when nbook is pusblisher")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 11,
                "title": "Book title number uno",
                "author": "Author name",
                "year": 2025
            }
        }
    }

class Library(BaseModel):
    name: str
    books: list[Book]

#valdiate json into Pydantic model
def library_data(filename):
    json_data = read_json(filename)
    return Library(**json_data)


if __name__ == "__main__":
    #print(read_json("library.json"))
    print(repr(library_data("library.json")))

