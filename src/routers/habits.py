from fastapi import APIRouter, Depends, status
from typing import List

from schemas.schemas import (
    HabitCreate,
    HabitUpdate,
    HabitOut,
    HabitProgress,
    TemplateUpdate,
    TemplateCreate,
    TemplateOut,
)
from apps.habits.habitsService import HabitsService
from utils.dependencies import get_current_user
from schemas.schemas import TokenData

router = APIRouter(prefix="/habits", tags=["habits"])

service = HabitsService()


@router.post("/", response_model=HabitOut, status_code=status.HTTP_201_CREATED)
async def create_habit(
    payload: HabitCreate, user: TokenData = Depends(get_current_user)
):
    return await service.create_habit(payload, user.user_id)


@router.get("/", response_model=List[HabitOut])
async def list_habits(user: TokenData = Depends(get_current_user)) -> List[HabitOut]:
    return await service.list_habits(user.user_id)


@router.put("/{habit_id}", response_model=HabitOut)
async def update_habit(
    habit_id: str,
    habit_update: HabitUpdate,
    current_user: TokenData = Depends(get_current_user),
):
    habit = await service.update_habit(habit_id, habit_update, current_user)
    return habit


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit(habit_id: str, user: TokenData = Depends(get_current_user)):
    await service.delete_habit(habit_id)
    return None


@router.get("/progress", response_model=List[HabitProgress])
async def get_progress(
    user: TokenData = Depends(get_current_user),
) -> List[HabitProgress]:
    return await service.get_progress(user.user_id)


# ----- CREAR PLANTILLA DE HÁBITO (ADMIN) -----
# (ojo, creo que no se esta revisando que sea admin)
@router.get("/templates", response_model=List[TemplateOut])
async def list_templates(
    user: TokenData = Depends(get_current_user),
) -> List[TemplateOut]:
    return await service.list_templates()


@router.post(
    "/templates", response_model=TemplateOut, status_code=status.HTTP_201_CREATED
)
async def create_template(
    payload: TemplateCreate, user: TokenData = Depends(get_current_user)
) -> TemplateOut:
    return await service.create_template(payload, user)


@router.patch("/templates/{template_id}", response_model=TemplateOut)
async def update_template(
    template_id: str,
    payload: TemplateUpdate,
    user: TokenData = Depends(get_current_user),
) -> TemplateOut:
    return await service.update_template(template_id, payload, user)


@router.delete("/templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(
    template_id: str, user: TokenData = Depends(get_current_user)
):
    await service.delete_template(template_id, user)
    return None
