from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.author import Author
from app.dependencies import get_current_user, require_admin
from pydantic import BaseModel

from datetime import date

router = APIRouter()


class AuthorCreate(BaseModel):
    name: str
    biography: str
    birth_date: date


class AuthorResponse(BaseModel):
    id: int
    name: str
    biography: str
    birth_date: date

    class Config:
        from_attributes = True


@router.post("/", response_model=AuthorResponse, dependencies=[Depends(require_admin)])
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    new_author = Author(**author.dict())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


@router.get("/", response_model=list[AuthorResponse])
def list_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = db.query(Author).offset(skip).limit(limit).all()
    return authors


@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.put("/{author_id}", response_model=AuthorResponse, dependencies=[Depends(require_admin)])
def update_author(author_id: int, author: AuthorCreate, db: Session = Depends(get_db)):
    existing_author = db.query(Author).filter(Author.id == author_id).first()
    if not existing_author:
        raise HTTPException(status_code=404, detail="Author not found")
    for key, value in author.dict().items():
        setattr(existing_author, key, value)
    db.commit()
    db.refresh(existing_author)
    return existing_author


@router.delete("/{author_id}", dependencies=[Depends(require_admin)])
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(author)
    db.commit()
    return {"message": "Author deleted successfully"}
