from pydantic import BaseModel

from datetime import date


class AuthorCreate(BaseModel):
    name: str
    biography: str
    birth_date: date


class AuthorResponse(AuthorCreate):
    id: int

    class Config:
        from_attributes = True
