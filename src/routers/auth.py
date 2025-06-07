import os
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict
from datetime import timedelta
import os

from models.models import User
from schemas.schemas import UserCreate, AdminCreate, UserOut, Token
from utils.auth_utils import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
)
from utils.dependencies import oauth2_scheme

router = APIRouter(prefix="/auth", tags=["auth"])


# ----- REGISTRO DE USUARIO -----
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate):
    existing = await User.find_one(User.email == user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está en uso"
        )
    hashed_pw = get_password_hash(user_in.password)
    user = User(
        email=user_in.email,
        hashed_password=hashed_pw,
        full_name=user_in.full_name,
        role="user",
    )
    await user.insert()
    return UserOut.from_orm(user)


# ----- REGISTRO DE ADMIN -----
@router.post(
    "/register-admin", response_model=UserOut, status_code=status.HTTP_201_CREATED
)
async def register_admin(admin_in: AdminCreate, token: str = Depends(oauth2_scheme)):
    # Solo un admin existente puede crear otro admin
    requester = decode_access_token(token)
    if not requester or requester.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sólo administradores pueden crear otros administradores",
        )

    existing = await User.find_one(User.email == admin_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está en uso"
        )
    hashed_pw = get_password_hash(admin_in.password)
    user = User(
        email=admin_in.email,
        hashed_password=hashed_pw,
        full_name=admin_in.full_name,
        role="admin",
    )
    await user.insert()
    return UserOut.from_orm(user)


# ----- LOGIN -----
@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: Dict[str, str]):
    """
    Se espera recibir JSON con {"email": "...", "password": "..."}
    """
    email = form_data.get("email")
    password = form_data.get("password")
    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email y contraseña requeridos",
        )
    user = await User.find_one(User.email == email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )
    # Generar token
    access_token_expires = timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    )
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role.value},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
