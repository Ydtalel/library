from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Author
from app.models.book import Book
from app.dependencies import require_admin
from app.schemas.book import BookResponse, BookCreate

router = APIRouter()


@router.post("/", response_model=BookResponse,
             dependencies=[Depends(require_admin)])
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Создает новую книгу с заданными авторами и данными"""
    authors = db.query(Author).filter(Author.id.in_(book.author_ids)).all()
    if not authors or len(authors) != len(book.author_ids):
        raise HTTPException(status_code=404,
                            detail="One or more authors not found")

    new_book = Book(
        title=book.title,
        description=book.description,
        published_date=book.published_date,
        available_copies=book.available_copies
    )
    new_book.authors = authors

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/", response_model=list[BookResponse])
def list_books(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    title: str = Query(None),
    author_name: str = Query(None),
):
    """Возвращает список книг с поддержкой пагинации и фильтрации"""
    query = db.query(Book)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author_name:
        query = query.join(Book.authors).filter(
            Author.name.ilike(f"%{author_name}%"))

    books = query.offset(skip).limit(limit).all()
    return books


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Возвращает информацию о конкретной книге по её ID"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookResponse,
            dependencies=[Depends(require_admin)])
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    """Обновляет данные книги по её ID"""
    existing_book = db.query(Book).filter(Book.id == book_id).first()
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(existing_book, key, value)
    db.commit()
    db.refresh(existing_book)
    return existing_book


@router.delete("/{book_id}", dependencies=[Depends(require_admin)])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Удаляет книгу по её ID"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}
