from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Модель данных для запроса на вход пользователя"""

    name: str
    password: str


class RegisterRequest(LoginRequest):
    """Модель данных для запроса на регистрацию нового пользователя"""

    email: str
