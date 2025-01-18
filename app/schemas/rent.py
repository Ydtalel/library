from pydantic import BaseModel
from datetime import date


class RentCreate(BaseModel):
    """Модель для создания аренды книги"""

    book_id: int
    return_date: date


class RentReturn(BaseModel):
    """Модель для возврата книги"""

    book_id: int
