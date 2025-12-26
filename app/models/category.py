from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models.base import Base


class Category(Base):
    __tablename__ = "categories"

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    books = relationship("Book", back_populates="category")
