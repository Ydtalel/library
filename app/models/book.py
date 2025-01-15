from sqlalchemy import Column, Integer, String, Table, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


book_author_association = Table(
    "book_author",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    published_date = Column(Date, nullable=True)
    available_copies = Column(Integer, default=1)

    authors = relationship("Author", secondary=book_author_association,
                           back_populates="books")
