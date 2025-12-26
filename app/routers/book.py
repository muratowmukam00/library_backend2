from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
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


from fastapi import Form
import json
from pydantic import ValidationError

@router.post(
    "",
    response_model=BookRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_book(
    data: str = Form(...),                 # ⬅️ ВАЖНО
    file: UploadFile | None = File(None),
    cover: UploadFile | None = File(None),
    _: User = Depends(get_current_admin),
    book_service: BookService = Depends(get_book_service),
    author_service: AuthorService = Depends(get_author_service),
):
    try:
        data_dict = json.loads(data)       # str → dict
        data_obj = BookCreate(**data_dict) # dict → Pydantic
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON in data field",
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=e.errors(),
        )

    author = author_service.get_author(data_obj.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    file_bytes = await file.read() if file else None
    cover_bytes = await cover.read() if cover else None

    return book_service.create_book(
        title=data_obj.title,
        description=data_obj.description,
        author_id=data_obj.author_id,
        file=file_bytes,
        file_name=file.filename if file else None,
        file_content_type=file.content_type if file else None,
        cover=cover_bytes,
        cover_name=cover.filename if cover else None,
        cover_content_type=cover.content_type if cover else None,
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


