from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.services.book_service import BookService
from app.services.author_service import AuthorService
from app.core.deps import (
    get_book_service,
    get_author_service,
    get_current_admin,
)
from app.models.user import User

router = APIRouter()


@router.post(
    "",
    response_model=BookRead,
    status_code=status.HTTP_201_CREATED,
)
def create_book(
    data: BookCreate,
    _: User = Depends(get_current_admin),
    book_service: BookService = Depends(get_book_service),
    author_service: AuthorService = Depends(get_author_service),
):
    author = author_service.get_author(data.author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found",
        )

    return book_service.create_book(
        title=data.title,
        description=data.description,
        author_id=data.author_id,
    )


@router.get(
    "",
    response_model=list[BookRead],
)
def list_books(
    skip: int = 0,
    limit: int = 100,
    _: User = Depends(get_current_admin),
    service: BookService = Depends(get_book_service),
):
    return service.list_books(skip=skip, limit=limit)


@router.get(
    "/{book_id}",
    response_model=BookRead,
)
def get_book(
    book_id: UUID,
    _: User = Depends(get_current_admin),
    service: BookService = Depends(get_book_service),
):
    book = service.get_book(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    return book


@router.patch(
    "/{book_id}",
    response_model=BookRead,
)
def update_book(
    book_id: UUID,
    data: BookUpdate,
    _: User = Depends(get_current_admin),
    book_service: BookService = Depends(get_book_service),
    author_service: AuthorService = Depends(get_author_service),
):
    book = book_service.get_book(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    update_data = data.model_dump(exclude_unset=True)

    if "author_id" in update_data:
        author = author_service.get_author(update_data["author_id"])
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author not found",
            )

    for field, value in update_data.items():
        setattr(book, field, value)

    return book_service.book_repo.update(book)


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_book(
    book_id: UUID,
    _: User = Depends(get_current_admin),
    service: BookService = Depends(get_book_service),
):
    book = service.get_book(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    service.delete_book(book)


