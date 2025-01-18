from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Rent, Book, Reader
from app.dependencies import get_current_user
from app.schemas.rent import RentCreate, RentReturn
from app.utils.logging import logger

router = APIRouter()


@router.post("/rent", response_model=dict)
def rent_book(
        rent_request: RentCreate,
        db: Session = Depends(get_db),
        current_user: Reader = Depends(get_current_user)
):
    book = db.query(Book).filter(Book.id == rent_request.book_id).first()
    if not book:
        logger.error(f"Rent failed: Book ID {rent_request.book_id} not found")
        raise HTTPException(status_code=404, detail="Book not found")

    if book.available_copies < 1:
        logger.error(f"Rent failed: No available copies for Book ID {book.id}")
        raise HTTPException(status_code=400,
                            detail="No available copies of this book")

    active_rents = db.query(Rent).filter(
        Rent.reader_id == current_user.id, Rent.return_date.is_(None)
    ).count()
    if active_rents >= 5:
        logger.error(
            f"Rent failed: User ID {current_user.id} exceeded the limit")
        raise HTTPException(
            status_code=400,
            detail="You cannot rent more than 5 books at a time"
        )

    rent = Rent(
        book_id=rent_request.book_id,
        reader_id=current_user.id,
        rent_date=date.today(),
        return_date=None
    )
    book.available_copies -= 1
    db.add(rent)
    db.commit()
    db.refresh(rent)
    logger.info(f"Book ID {book.id} rented by User ID {current_user.id}")
    return {"message": "Book rented successfully"}


@router.post("/return", response_model=dict)
def return_book(
        return_request: RentReturn,
        db: Session = Depends(get_db),
        current_user: Reader = Depends(get_current_user)
):
    rent = db.query(Rent).filter(
        Rent.book_id == return_request.book_id,
        Rent.reader_id == current_user.id,
        Rent.return_date.is_(None)
    ).first()
    if not rent:
        logger.error(
            "Return failed: No active rent for Book ID "
            f"{return_request.book_id}")
        raise HTTPException(status_code=404,
                            detail="No active rent found for this book")

    rent.return_date = date.today()
    book = db.query(Book).filter(Book.id == return_request.book_id).first()
    if book:
        book.available_copies += 1

    db.commit()
    logger.info(f"Book ID {book.id} returned by User ID {current_user.id}")
    return {"message": "Book returned successfully"}
