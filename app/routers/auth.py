from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.reader import Reader
from app.schemas.auth import RegisterRequest, LoginRequest
from app.utils.utils import hash_password, verify_password, create_access_token


router = APIRouter()


@router.post("/register")
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    user = db.query(Reader).filter(Reader.name == request.name).first()
    if user:
        raise HTTPException(status_code=400, detail="name already exists")

    hashed_password = hash_password(request.password)
    new_user = Reader(
        name=request.name,
        email=request.email,
        hashed_password=hashed_password,
        is_admin=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}


@router.post("/login")
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Reader).filter(Reader.name == request.name).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.name})
    return {"access_token": token, "token_type": "bearer"}
