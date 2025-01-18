from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.utils.utils import decode_access_token
from app.database import get_db
from app.models.reader import Reader

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)) -> Reader:
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials")
    payload = decode_access_token(token)
    if not payload:
        raise credentials_exception
    name = payload.get("sub")
    if not name:
        raise credentials_exception
    user = db.query(Reader).filter(Reader.name == name).first()
    if not user:
        raise credentials_exception
    return user


def require_admin(current_user: Reader = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You do not have permission to perform this action")
    return current_user
