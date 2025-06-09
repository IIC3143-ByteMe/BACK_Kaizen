from fastapi import APIRouter, Depends

from models.models import User
from schemas.schemas import UserOut
from utils.dependencies import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


# ----- REGISTRO DE USUARIO -----
@router.get("/", response_model=UserOut)
async def get_user_info(current_user=Depends(get_current_user)):
    user = await User.get(current_user.user_id)
    return UserOut.from_orm(user)
