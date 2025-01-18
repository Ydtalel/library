from pydantic import BaseModel
from datetime import date


class BookCreate(BaseModel):
    title: str
    description: str
    published_date: date
    available_copies: int
    author_ids: list[int]

    class Config:
        from_attributes = True


class BookResponse(BaseModel):
    id: int
