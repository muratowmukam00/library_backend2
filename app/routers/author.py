from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from app.schemas.author import (
    AuthorCreate,
    AuthorRead,
    AuthorUpdate,
)
from app.services.author_service import AuthorService
from app.core.deps import get_author_service, get_current_admin
from app.models.user import User

router = APIRouter()

@router.post(
    "",
    response_model=AuthorRead,
    status_code=status.HTTP_201_CREATED,
)
def create_author(
    data: AuthorCreate,
    _: User = Depends(get_current_admin),
    service: AuthorService = Depends(get_author_service),
):
    return service.create_author(
        name=data.name,
        biography=data.biography,
    )


@router.get(
    "",
    response_model=list[AuthorRead],
)
def list_authors(
    service: AuthorService = Depends(get_author_service),
):
    return service.list_authors()


@router.get(
    "/{author_id}",
    response_model=AuthorRead,
)
def get_author(
    author_id: UUID,
    service: AuthorService = Depends(get_author_service),
):
    author = service.get_author(author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found",
        )
    return author



@router.put(
    "/{author_id}",
    response_model=AuthorRead,
)
def update_author(
    author_id: UUID,
    data: AuthorUpdate,
    _: User = Depends(get_current_admin),
    service: AuthorService = Depends(get_author_service),
):
    author = service.get_author(author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found",
        )

    update_data = data.model_dump(exclude_unset=True)
    return service.update_author(author, update_data)


@router.delete(
    "/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_author(
    author_id: UUID,
    _: User = Depends(get_current_admin),
    service: AuthorService = Depends(get_author_service),
):
    author = service.get_author(author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found",
        )

    service.delete_author(author)
