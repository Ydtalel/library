from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.author import Author
from app.dependencies import require_admin
from app.schemas.author import AuthorResponse, AuthorCreate

router = APIRouter()


@router.post("/", response_model=AuthorResponse,
             dependencies=[Depends(require_admin)])
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    """Создает нового автора и сохраняет его в базе данных"""
    new_author = Author(**author.dict())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


@router.get("/", response_model=list[AuthorResponse])
def list_authors(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    name: str = Query(None),
):
    """Возвращает список авторов с поддержкой пагинации и фильтрации"""
    query = db.query(Author)
    if name:
        query = query.filter(Author.name.ilike(f"%{name}%"))
    authors = query.offset(skip).limit(limit).all()
    return authors


@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    """Возвращает информацию о конкретном авторе по его ID"""
    author = db.query(Author).filter(Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.put("/{author_id}", response_model=AuthorResponse,
            dependencies=[Depends(require_admin)])
def update_author(author_id: int, author: AuthorCreate,
                  db: Session = Depends(get_db)):
    """Обновляет данные автора по его ID"""
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
    """Удаляет автора по его ID"""
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(author)
    db.commit()
    return {"message": "Author deleted successfully"}
