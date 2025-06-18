from typing import Optional
from models.models import IkigaiEducation


class IkigaiDBRepository:
    async def create_content(self, data: dict) -> IkigaiEducation:
        content = IkigaiEducation(**data)
        await content.insert()
        return content

    async def get_content_by_owner(self, owner_id: str) -> Optional[IkigaiEducation]:
        return await IkigaiEducation.find_one(IkigaiEducation.owner_id == owner_id)

    async def get_content_by_id(self, content_id: str) -> Optional[IkigaiEducation]:
        return await IkigaiEducation.get(content_id)

    async def update_content(
        self, content: IkigaiEducation, changes: dict
    ) -> IkigaiEducation:
        await content.set(changes)
        return content

    async def delete_content(self, content: IkigaiEducation) -> None:
        await content.delete()
