from fastapi import APIRouter
from typing import Dict
from schemas.roles import Token
from apps.auth.authService import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
service = AuthService()


@router.post("/login", response_model=Token)
async def login(form_data: Dict[str, str]):
    return await service.login_for_access_token(form_data)
