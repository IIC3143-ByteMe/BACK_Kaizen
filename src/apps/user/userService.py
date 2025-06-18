
from fastapi import HTTPException, status, Depends
from schemas.schemas import UserOut
from utils.dependencies import get_current_user, TokenData
from apps.user.userDBRepository import UserDBRepository


class UserService:
    def __init__(self):
        self.repo = UserDBRepository()

    async def get_user_info(
        self,
        user: TokenData
    ) -> UserOut:
        db_user = await self.repo.get_by_id(user.user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return UserOut.from_orm(db_user)