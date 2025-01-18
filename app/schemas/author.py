from pydantic import BaseModel

from datetime import date


class AuthorCreate(BaseModel):
    """Модель данных для создания нового автора"""

    name: str
    biography: str
    birth_date: date


class AuthorResponse(AuthorCreate):
    """Модель данных для ответа с информацией об авторе"""

    id: int

    class Config:
        from_attributes = True
