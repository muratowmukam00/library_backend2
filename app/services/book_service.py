from app.models.book import Book
from app.repositories.book_repo import BookRepository
from app.services.storage_service import StorageService

class BookService:
    def __init__(self, book_repo: BookRepository, storage_service: StorageService):
        self.book_repo = book_repo
        self.storage_service = storage_service

    def create_book(
        self,
        title: str,
        description: str,
        author_id,
        file: bytes | None = None,
        file_name: str | None = None,
        file_content_type: str | None = None,
        cover: bytes | None = None,
        cover_name: str | None = None,
        cover_content_type: str | None = None,
    ):
        file_url = None
        cover_url = None

        if file and file_name:
            file_url = self.storage_service.upload_file(file, file_name, file_content_type)

        if cover and cover_name:
            cover_url = self.storage_service.upload_file(cover, cover_name, cover_content_type)

        book = Book(
            title=title,
            description=description,
            author_id=author_id,
            file_url=file_url,
            image_url=cover_url,
        )
        return self.book_repo.create(book)

    def get_book(self, book_id):
        return self.book_repo.get_by_id(book_id)

    def list_books(self, skip: int = 0, limit: int = 100):
        return self.book_repo.list_all(skip=skip, limit=limit)

    def update_book(self, book: Book, update_data: dict, file: bytes | None = None, file_name: str | None = None,
                    cover: bytes | None = None, cover_name: str | None = None):
        # Faýllary üýtgetmek
        if file and file_name:
            if book.file_url:
                old_file_name = book.file_url.split("/")[-1]
                self.storage_service.delete_file(old_file_name)
            book.file_url = self.storage_service.upload_file(file, file_name)

        if cover and cover_name:
            if book.image_url:
                old_cover_name = book.image_url.split("/")[-1]
                self.storage_service.delete_file(old_cover_name)
            book.image_url = self.storage_service.upload_file(cover, cover_name)

        for field, value in update_data.items():
            setattr(book, field, value)

        return self.book_repo.update(book)

    def delete_book(self, book: Book):
        # Faýllary pozmak
        if book.file_url:
            old_file_name = book.file_url.split("/")[-1]
            self.storage_service.delete_file(old_file_name)

        if book.image_url:
            old_cover_name = book.image_url.split("/")[-1]
            self.storage_service.delete_file(old_cover_name)

        return self.book_repo.delete(book)
