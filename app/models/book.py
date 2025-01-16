from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.author import book_author_association


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    published_date = Column(Date, nullable=True)
    available_copies = Column(Integer, default=1, nullable=False)

    authors = relationship("Author", secondary=book_author_association,
                           back_populates="books")

    rents = relationship("Rent", back_populates="book")
