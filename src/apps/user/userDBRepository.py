from typing import Optional
from models.models import User


class UserDBRepository:
    async def get_by_id(self, user_id: str) -> Optional[User]:
        return await User.get(user_id)
