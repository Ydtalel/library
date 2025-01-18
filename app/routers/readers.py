from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.reader import Reader
from app.dependencies import require_admin, get_current_user
from app.schemas.reader import ReaderResponse, ReaderUpdate

router = APIRouter()


@router.get("/", response_model=list[ReaderResponse])
def get_all_readers(db: Session = Depends(get_db),
                    current_user: Reader = Depends(require_admin)):
    """
    Возвращает список всех читателей. Только для администратора.
    """
    readers = db.query(Reader).all()
    return readers


@router.put("/me", response_model=ReaderResponse)
def update_reader_info(
        reader_update: ReaderUpdate,
        db: Session = Depends(get_db),
        current_user: Reader = Depends(get_current_user),
):
    """
    Обновляет информацию о текущем читателе.
    """
    current_user.name = reader_update.name
    current_user.email = reader_update.email

    db.commit()
    db.refresh(current_user)
    return current_user
