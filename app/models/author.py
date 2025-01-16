from sqlalchemy import Column, Integer, String, Text, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

book_author_association = Table(
    "book_author",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    biography = Column(Text, nullable=True)
    birth_date = Column(Date, nullable=True)

    books = relationship("Book", secondary=book_author_association,
                         back_populates="authors")
