from sqlalchemy import Column, String
from app.models.base import Base

class Author(Base):
    __tablename__ = "authors"

    name = Column(String(100), nullable=False)
    biography = Column(String(500))
