from fastapi import APIRouter, Depends, HTTPException, status

from models.models import IkigaiEducation
from schemas.schemas import IkigaiEducationCreate, IkigaiEducationOut
from utils.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/ikigai", tags=["ikigai"])


# ----- CREAR CONTENIDO EDUCATIVO (ADMIN) -----
@router.post(
    "/", response_model=IkigaiEducationOut, status_code=status.HTTP_201_CREATED
)
async def create_ikigai_content(
    content_in: IkigaiEducationCreate, current_user=Depends(get_current_user)
):
    content = content_in.dict()
    content["owner_id"] = current_user.user_id
    new_ikigai = IkigaiEducation(**content)
    await new_ikigai.insert()
    return IkigaiEducationOut.from_orm(new_ikigai)


# ----- LISTAR TODO EL CONTENIDO (CUALQUIER USUARIO) -----
@router.get("/", response_model=IkigaiEducationOut)
async def list_ikigai_content(current_user=Depends(get_current_user)):
    contents = await IkigaiEducation.find_one(
        IkigaiEducation.owner_id == current_user.user_id
    )
    try:
        return IkigaiEducationOut.from_orm(contents)
    except():
        raise ValueError
    

# ----- MODIFICAR CONTENIDO (usuario) -----
@router.put("/", response_model=IkigaiEducationOut)
async def update_ikigai_content(
    content_in: IkigaiEducationCreate,
    current_user=Depends(get_current_user),
):
    content = await IkigaiEducation.find_one(
        IkigaiEducation.owner_id == current_user.user_id
    )
    if not content:
        raise HTTPException(status_code=404, detail="Contenido no encontrado")

    content.arquetipo = content_in.arquetipo
    content.amas = content_in.amas
    content.bueno = content_in.bueno
    content.necesita = content_in.necesita
    content.pagar = content_in.pagar

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
