from sqlalchemy.orm import Session
from app.models.author import Author

class AuthorRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, author: Author):
        self.db.add(author)
        self.db.commit()
        self.db.refresh(author)
        return author

    def get_by_id(self, author_id):
        return self.db.query(Author).filter(Author.id == author_id).first()

    def get_by_name(self, name: str):
        return self.db.query(Author).filter(Author.name == name).first()

    def list_all(self):
        return self.db.query(Author).all()

    def delete(self, author: Author):
        self.db.delete(author)
        self.db.commit()


    def update(self, author: Author):
        self.db.add(author)
        self.db.commit()
        self.db.refresh(author)
        return author