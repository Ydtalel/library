from pydantic import BaseModel
from datetime import date


class BookBase(BaseModel):
    title: str
    description: str
    published_date: date
    available_copies: int

    class Config:
        from_attributes = True


class BookCreate(BookBase):
    author_ids: list[int]


class AuthorResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class BookResponse(BookBase):
    id: int
    authors: list[AuthorResponse]
