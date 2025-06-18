from fastapi import APIRouter, Depends, status
from typing import Dict
from schemas.schemas import UserCreate, AdminCreate, UserOut, Token
from utils.dependencies import oauth2_scheme
from apps.auth.authService import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
service = AuthService()

@router.post(
    "/register", response_model=UserOut, status_code=status.HTTP_201_CREATED
)
async def register_user(user_in: UserCreate):
    return await service.register_user(user_in)

@router.post(
    "/register-admin", response_model=UserOut, status_code=status.HTTP_201_CREATED
)
async def register_admin(
    admin_in: AdminCreate,
    token: str = Depends(oauth2_scheme)
):
    return await service.register_admin(admin_in, token)

@router.post("/login", response_model=Token)
async def login(form_data: Dict[str, str]):
    return await service.login_for_access_token(form_data)