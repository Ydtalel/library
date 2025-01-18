from pydantic import BaseModel


class ReaderUpdate(BaseModel):
    """Модель для обновления данных пользователя"""

    name: str
    email: str

    class Config:
        from_attributes = True


class ReaderResponse(ReaderUpdate):
    """Ответ с информацией о пользователе"""

    is_active: bool
    is_admin: bool
