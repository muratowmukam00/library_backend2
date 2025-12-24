# app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserRead
from app.schemas.auth import TokenResponse, RefreshTokenRequest, LoginRequest
from app.services.user_service import UserService
from app.core import security
from app.core.deps import get_user_service
router = APIRouter()


@router.post("/register", response_model=UserRead)
def register(user_in: UserCreate, user_service: UserService = Depends(get_user_service)):
    role = UserRole.user
    if not user_service.list_users():
        role = UserRole.admin

    if user_service.get_by_email(user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")


    user = user_service.create_user(
        email=user_in.email,
        password=user_in.password,
        role=role.value
    )
    return user


@router.post("/login", response_model=TokenResponse)
def login(
    login_data: LoginRequest,
    user_service: UserService = Depends(get_user_service)
):
    user = user_service.get_by_email(login_data.email)
    if not user or not security.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = security.create_access_token(str(user.id))
    refresh_token = security.create_refresh_token(str(user.id))
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


# Refresh token endpoint
@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_request: RefreshTokenRequest):
    try:
        payload = security.decode_token(refresh_request.refresh_token)
        user_id = payload.get("sub")
        access_token = security.create_access_token(user_id)
        refresh_token = security.create_refresh_token(user_id)
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout")
def logout():
    return {"msg": "Successfully logged out"}
