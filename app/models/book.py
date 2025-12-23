from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Book(Base):
    __tablename__ = "books"

    title = Column(String(255), nullable=False)
    description = Column(String(500))
    author_id = Column(ForeignKey("authors.id"))

    author = relationship("Author", backref="books")
