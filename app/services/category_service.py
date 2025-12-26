from fastapi import HTTPException, status

from app.repositories.category_repo import CategoryRepository
from app.models.category import Category


class CategoryService:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    def create_category(self, name: str, description: str | None = None):
        if self.category_repo.get_by_name(name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category with this name already exists",
            )
        category = Category(name=name, description=description)
        return self.category_repo.create(category)
    def get_category(self, category_id: int):
        return self.category_repo.get_by_id(category_id)

    def list_categories(self):
        return self.category_repo.list_all()

    def update_category(self, category: Category, data: dict):
        for field, value in data.items():
            setattr(category, field, value)
        return self.category_repo.update(category)

    def delete_category(self, category: Category):
        return self.category_repo.delete(category)
