from pydantic import BaseModel


class LoginRequest(BaseModel):
    name: str
    password: str


class RegisterRequest(LoginRequest):
    email: str
