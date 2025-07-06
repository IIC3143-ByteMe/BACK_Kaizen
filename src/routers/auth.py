from fastapi import APIRouter, status
from typing import Dict
from schemas.requests import UserCreate
from schemas.roles import UserOut, Token
from apps.auth.authService import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
service = AuthService()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate):
    return await service.register_user(user_in)


@router.post("/login", response_model=Token)
async def login(form_data: Dict[str, str]):
    return await service.login_for_access_token(form_data)
