from fastapi import HTTPException, status
from schemas.schemas import IkigaiEducationCreate, IkigaiEducationOut, TokenData
from apps.ikigai.ikigaiDBRepository import IkigaiDBRepository


class IkigaiService:
    def __init__(self):
        self.repo = IkigaiDBRepository()

    async def create_content(
        self, payload: IkigaiEducationCreate, user: TokenData
    ) -> IkigaiEducationOut:
        data = payload.dict()
        data["owner_id"] = user.user_id
        content = await self.repo.create_content(data)
        return IkigaiEducationOut.from_orm(content)

    async def get_content(self, user: TokenData) -> IkigaiEducationOut:
        content = await self.repo.get_content_by_owner(user.user_id)
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Contenido no encontrado"
            )
        return IkigaiEducationOut.from_orm(content)

    async def update_content(
        self, payload: IkigaiEducationCreate, user: TokenData
    ) -> IkigaiEducationOut:
        content = await self.repo.get_content_by_owner(user.user_id)
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Contenido no encontrado"
            )
        changes = payload.dict(exclude_unset=True)
        updated = await self.repo.update_content(content, changes)
        return IkigaiEducationOut.from_orm(updated)

    async def delete_content(self, content_id: str) -> None:
        content = await self.repo.get_content_by_id(content_id)
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Contenido no encontrado"
            )
        await self.repo.delete_content(content)
