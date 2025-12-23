from app.repositories.book_repo import BookRepository
from app.models.book import Book

class BookService:
    def __init__(self, book_repo: BookRepository):
        self.book_repo = book_repo

    def create_book(self, title: str, description: str, author_id, file_url: str = None, cover_url: str = None):
        book = Book(
            title=title,
            description=description,
            author_id=author_id,
            # file_url=file_url,
            # cover_url=cover_url
        )
        return self.book_repo.create(book)

    def get_book(self, book_id):
        return self.book_repo.get_by_id(book_id)

    def list_books(self, skip: int = 0, limit: int = 100):
        return self.book_repo.list_all(skip=skip, limit=limit)

    def delete_book(self, book):
        return self.book_repo.delete(book)
