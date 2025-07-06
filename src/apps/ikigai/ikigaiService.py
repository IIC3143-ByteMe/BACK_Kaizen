from fastapi import HTTPException, status
from schemas.users import IkigaiEducation, IkigaiEducationCreate, IkigaiEducationUpdate
from schemas.roles import TokenData
from apps.ikigai.ikigaiDBRepository import IkigaiDBRepository


class IkigaiService:
    def __init__(self):
        self.repo = IkigaiDBRepository()

    async def create_content(
        self, payload: IkigaiEducationCreate, user: TokenData
    ) -> IkigaiEducation:
        data = payload.model_dump()
        content = await self.repo.create_content(user.user_id, data)
        return IkigaiEducation.model_validate(content)

    async def get_content(self, user: TokenData) -> IkigaiEducation:
        content = await self.repo.get_content_by_owner(user.user_id)
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Contenido no encontrado"
            )
        return IkigaiEducation.model_validate(content)

    async def update_content(
        self, payload: IkigaiEducationUpdate, user: TokenData
    ) -> IkigaiEducation:
        content = await self.repo.get_content_by_owner(user.user_id)
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Contenido no encontrado"
            )
        changes = payload.model_dump(exclude_unset=True)
        [setattr(content, k, v) for k, v in changes.items() if hasattr(content, k)]

        updated = await self.repo.update_content(user.user_id, content)
        return IkigaiEducation.model_validate(updated)

    async def delete_content(self, content_id: str) -> None:
        content = await self.repo.get_content_by_id(content_id)
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Contenido no encontrado"
            )
        await self.repo.delete_content(content)
