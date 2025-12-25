from sqlalchemy.orm import Session
from app.models.book import Book

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, book: Book):
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def get_by_id(self, book_id):
        return self.db.query(Book).filter(Book.id == book_id).first()

    def get_by_title(self, title: str):
        return self.db.query(Book).filter(Book.title == title).first()

    def list_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Book).offset(skip).limit(limit).all()

    def delete(self, book: Book):
        self.db.delete(book)
        self.db.commit()

    def update(self, book: Book):
        self.db.add(book)
        self.db.commit()
        return book