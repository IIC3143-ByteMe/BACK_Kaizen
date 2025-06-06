from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from models.models import IkigaiEducation
from schemas.schemas import IkigaiEducationCreate, IkigaiEducationOut
from utils.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/ikigai", tags=["ikigai"])

# ----- CREAR CONTENIDO EDUCATIVO (ADMIN) -----
@router.post("/", response_model=IkigaiEducationOut, status_code=status.HTTP_201_CREATED)
async def create_ikigai_content(
    content_in: IkigaiEducationCreate,
    current_admin=Depends(require_admin)
):
    content = IkigaiEducation(
        title=content_in.title,
        content=content_in.content
    )
    await content.insert()
    return IkigaiEducationOut.from_orm(content)

# ----- LISTAR TODO EL CONTENIDO (CUALQUIER USUARIO) -----
@router.get("/", response_model=List[IkigaiEducationOut])
async def list_ikigai_content(current_user=Depends(get_current_user)):
    contents = await IkigaiEducation.find_all().to_list()
    return [IkigaiEducationOut.from_orm(c) for c in contents]

# ----- MODIFICAR CONTENIDO (ADMIN) -----
@router.put("/{content_id}", response_model=IkigaiEducationOut)
async def update_ikigai_content(
    content_id: str,
    content_in: IkigaiEducationCreate,
    current_admin=Depends(require_admin)
):
    content = await IkigaiEducation.get(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Contenido no encontrado")
    content.title = content_in.title
    content.content = content_in.content
    await content.save()
    return IkigaiEducationOut.from_orm(content)

# ----- ELIMINAR CONTENIDO (ADMIN) -----
@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ikigai_content(content_id: str, current_admin=Depends(require_admin)):
    content = await IkigaiEducation.get(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Contenido no encontrado")
    await content.delete()
    return None
