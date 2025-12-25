# app/services/author_service.py
from app.repositories.author_repo import AuthorRepository
from app.models.author import Author

class AuthorService:
    def __init__(self, author_repo: AuthorRepository):
        self.author_repo = author_repo

    def create_author(self, name: str, biography: str | None = None):
        author = Author(name=name, biography=biography)
        return self.author_repo.create(author)

    def get_author(self, author_id):
        return self.author_repo.get_by_id(author_id)

    def list_authors(self):
        return self.author_repo.list_all()

    def update_author(self, author: Author, data: dict):
        for field, value in data.items():
            setattr(author, field, value)
        return self.author_repo.update(author)

    def delete_author(self, author: Author):
        return self.author_repo.delete(author)
