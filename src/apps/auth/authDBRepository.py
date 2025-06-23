from typing import Optional
from models.models import User


class AuthDBRepository:
    async def find_by_email(self, email: str) -> Optional[User]:
        return await User.find_one(User.email == email)

    async def insert_user(self, data: dict) -> User:
        user = User(**data)
        await user.insert()
        return user
