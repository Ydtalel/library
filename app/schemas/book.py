from pydantic import BaseModel
from datetime import date


class BookBase(BaseModel):
    """Базовая модель данных для книги"""

    title: str
    description: str
    published_date: date
    available_copies: int

    class Config:
        from_attributes = True


class BookCreate(BookBase):
    """Модель для создания книги"""

    author_ids: list[int]


class AuthorResponse(BaseModel):
    """Ответ с информацией об авторе"""

    id: int
    name: str

    class Config:
        from_attributes = True


class BookResponse(BookBase):
    """Ответ с информацией о книге"""

    id: int
    authors: list[AuthorResponse]
