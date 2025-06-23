from fastapi import APIRouter, Depends, status
from schemas.schemas import IkigaiEducationCreate, IkigaiEducationOut
from utils.dependencies import get_current_user, require_admin, TokenData
from apps.ikigai.ikigaiService import IkigaiService

router = APIRouter(prefix="/ikigai", tags=["ikigai"])
service = IkigaiService()


@router.post(
    "/", response_model=IkigaiEducationOut, status_code=status.HTTP_201_CREATED
)
async def create_ikigai_content(
    payload: IkigaiEducationCreate, user: TokenData = Depends(get_current_user)
) -> IkigaiEducationOut:
    return await service.create_content(payload, user)


@router.get("/", response_model=IkigaiEducationOut)
async def get_ikigai_content(
    user: TokenData = Depends(get_current_user),
) -> IkigaiEducationOut:
    return await service.get_content(user)


@router.put("/", response_model=IkigaiEducationOut)
async def update_ikigai_content(
    payload: IkigaiEducationCreate, user: TokenData = Depends(get_current_user)
) -> IkigaiEducationOut:
    return await service.update_content(payload, user)


@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ikigai_content(
    content_id: str, admin: TokenData = Depends(require_admin)
):
    # require_admin ensures only admins reach here
    await service.delete_content(content_id)
    return None
