from pydantic import BaseModel
from datetime import date


class RentCreate(BaseModel):
    book_id: int
    return_date: date


class RentReturn(BaseModel):
    book_id: int
