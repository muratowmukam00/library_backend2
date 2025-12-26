from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core import security
from app.core.database import get_db
from app.core.security import  bearer_scheme
from app.models.user import UserRole
from app.repositories.author_repo import AuthorRepository
from app.repositories.book_repo import BookRepository
from app.repositories.category_repo import CategoryRepository
from app.repositories.user_repo import UserRepository
from app.services.author_service import AuthorService
from app.services.book_service import BookService
from app.services.category_service import CategoryService
from app.services.user_service import UserService


def get_user_service(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)

async def get_current_user(
    credentials = Depends(bearer_scheme),
    user_service: UserService = Depends(get_user_service),
):
    token = credentials.credentials
    try:
        payload = security.decode_token(token)
        user_id: str | None = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        user = user_service.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        return user

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

async def get_current_admin(
    current_user = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    return current_user

def get_author_service(db: Session = Depends(get_db)):
    repo = AuthorRepository(db)
    return AuthorService(repo)

def get_book_service(db: Session = Depends(get_db)):
    repo = BookRepository(db)
    return BookService(repo)

def get_category_service(db: Session = Depends(get_db)):
    repo = CategoryRepository(db)
    return CategoryService(repo)