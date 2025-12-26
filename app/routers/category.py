from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from app.schemas.category import (
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
)
from app.services.category_service import CategoryService
from app.core.deps import get_category_service, get_current_admin
from app.models.user import User

router = APIRouter()

@router.post(
    "",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    data: CategoryCreate,
    _: User = Depends(get_current_admin),
    service: CategoryService = Depends(get_category_service),
):
    return service.create_category(
        name=data.name,
        description=data.description,
    )


@router.get(
    "",
    response_model=list[CategoryRead],
)
def list_categories(
    service: CategoryService = Depends(get_category_service),
):
    return service.list_categories()


@router.get(
    "/{category_id}",
    response_model=CategoryRead,
)
def get_category(
    category_id: UUID,
    service: CategoryService = Depends(get_category_service),
):
    category = service.get_category(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category


@router.put(
    "/{category_id}",
    response_model=CategoryRead,
)
def update_category(
    category_id: UUID,
    data: CategoryUpdate,
    _: User = Depends(get_current_admin),
    service: CategoryService = Depends(get_category_service),
):
    category = service.get_category(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    update_data = data.model_dump(exclude_unset=True)
    return service.update_category(category, update_data)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id: UUID,
    _: User = Depends(get_current_admin),
    service: CategoryService = Depends(get_category_service),
):
    category = service.get_category(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    service.delete_category(category)
