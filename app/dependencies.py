from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from app.utils import decode_access_token
from app.database import get_db
from app.models.reader import Reader

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials")
    payload = decode_access_token(token)
    if not payload:
        raise credentials_exception
    username = payload.get("sub")
    if not username:
        raise credentials_exception
    user = db.query(Reader).filter(Reader.username == username).first()
    if not user:
        raise credentials_exception
    return user
