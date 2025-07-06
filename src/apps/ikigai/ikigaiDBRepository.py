from beanie.operators import Set
from typing import Optional
from models.models import IkigaiEducation, User


class IkigaiDBRepository:
    async def create_content(self, user_id: str, data: dict) -> IkigaiEducation:
        content = IkigaiEducation(**data)
        user = await User.get(user_id)
        await user.update(Set({User.ikigai: content}))

        return content

    async def get_content_by_owner(self, owner_id: str) -> Optional[IkigaiEducation]:
        user = await User.get(owner_id)
        ikigai = user.ikigai
        return ikigai

    async def get_content_by_id(self, content_id: str) -> Optional[IkigaiEducation]:
        return await IkigaiEducation.get(content_id)

    async def update_content(
        self, user_id: str, changes: IkigaiEducation
    ) -> IkigaiEducation:

        print("AQUIII")
        print(changes)

        user = await User.get(user_id)
        await user.update(Set({User.ikigai: changes}))
        user = await User.get(user_id)

        ikigai = user.ikigai
        return ikigai

    async def delete_content(self, user_id) -> None:
        await User.find_one(User.id == user_id).update(Set({User.ikigai: None}))
