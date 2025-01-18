from pydantic import BaseModel


class ReaderUpdate(BaseModel):
    name: str
    email: str

    class Config:
        from_attributes = True


class ReaderResponse(ReaderUpdate):
    is_active: bool
    is_admin: bool
