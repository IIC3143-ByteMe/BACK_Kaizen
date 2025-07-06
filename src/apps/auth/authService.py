import os
from datetime import timedelta
from fastapi import HTTPException, status, Depends
from typing import Dict
from schemas.roles import UserOut, Token
from schemas.requests import UserCreate, AdminCreate

from utils.auth_utils import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
)
from utils.dependencies import oauth2_scheme
from apps.auth.authDBRepository import AuthDBRepository


class AuthService:
    def __init__(self):
        self.repo = AuthDBRepository()
        self.expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    async def register_user(self, payload: UserCreate) -> UserOut:
        existing = await self.repo.find_by_email(payload.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo ya está en uso",
            )
        data = payload.dict()
        data["hashed_password"] = get_password_hash(data.pop("password"))
        data["role"] = "user"
        user = await self.repo.insert_user(data)
        return UserOut.from_orm(user)

    async def register_admin(
        self, payload: AdminCreate, token: str = Depends(oauth2_scheme)
    ) -> UserOut:
        requester = decode_access_token(token)
        if not requester or requester.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sólo administradores pueden crear otros administradores",
            )
        existing = await self.repo.find_by_email(payload.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo ya está en uso",
            )
        data = payload.dict()
        data["hashed_password"] = get_password_hash(data.pop("password"))
        data["role"] = "admin"
        user = await self.repo.insert_user(data)
        return UserOut.from_orm(user)

    async def login_for_access_token(self, form_data: Dict[str, str]) -> Token:
        email = form_data.get("email")
        password = form_data.get("password")
        if not email or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email y contraseña requeridos",
            )
        user = await self.repo.find_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
            )
        access_token_expires = timedelta(minutes=self.expire_minutes)
        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role},
            expires_delta=access_token_expires,
        )
        return Token(access_token=access_token, token_type="bearer")
