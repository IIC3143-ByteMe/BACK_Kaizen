from fastapi import APIRouter, Depends
from schemas.roles import UserOut, TokenData
from utils.dependencies import get_current_user
from apps.user.userService import UserService

router = APIRouter(prefix="/user", tags=["user"])
service = UserService()


@router.get("/", response_model=UserOut)
async def get_user_info(user: TokenData = Depends(get_current_user)) -> UserOut:
    return await service.get_user_info(user)
