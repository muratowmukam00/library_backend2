# app/api/auth.py
import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.models.user import UserRole
from app.schemas.user import UserCreate, UserRead
from app.schemas.auth import TokenResponse, RefreshTokenRequest, LoginRequest, LogoutRequest
from app.services.user_service import UserService
from app.services.redis_service import RedisService
from app.core import security
from app.core.deps import get_user_service, get_current_user
from app.core.config import settings

router = APIRouter()
redis_service = RedisService()
expire_seconds = settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60
@router.post("/register", response_model=UserRead)
def register(user_in: UserCreate, user_service: UserService = Depends(get_user_service)):
    role = UserRole.user
    if not user_service.list_users():
        role = UserRole.admin

    if user_service.get_by_email(user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")


    user = user_service.create_user(
        full_name=user_in.full_name,
        email=user_in.email,
        password=user_in.password,
        role=role.value
    )
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    user_service: UserService = Depends(get_user_service)
):
    user = user_service.get_by_email(login_data.email)
    if not user or not security.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = security.create_access_token(str(user.id))
    refresh_token = security.create_refresh_token(str(user.id))

    redis_key = f"refresh:{refresh_token}"

    await redis_service.set(redis_key, str(user.id), expire=expire_seconds)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_request: RefreshTokenRequest):
    try:
        redis_key = f"refresh:{refresh_request.refresh_token}"
        token_exists = await redis_service.exists(redis_key)
        if not token_exists:
            raise HTTPException(status_code=401, detail="Refresh token not found or expired")

        user_id = await redis_service.get(redis_key)
        access_token = security.create_access_token(user_id)
        new_refresh_token = security.create_refresh_token(user_id)

        await redis_service.delete(redis_key)
        await redis_service.set(f"refresh:{new_refresh_token}", user_id, expire=expire_seconds)

        return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout")
async def logout(
    data: LogoutRequest,
):
    redis_key = f"refresh:{data.refresh_token}"

    token_exists = await redis_service.exists(redis_key)
    if token_exists:
        await redis_service.delete(redis_key)

    return {"msg": "Successfully logged out"}

@router.get("/me")
def me(current_user = Depends(get_current_user)):
    return current_user

