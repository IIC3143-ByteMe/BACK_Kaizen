from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from models.models import DailyCompletions, Habit
from schemas.habits import HabitCreate, HabitUpdate, HabitOut, HabitProgress
from schemas.templates import (
    TemplateHabitCreate,
    TemplateHabitOut,
    TemplateHabitUpdate,
)
from apps.habits.habitsService import HabitsService
from utils.dependencies import get_current_user
from schemas.roles import TokenData

router = APIRouter(prefix="/habits", tags=["habits"])

service = HabitsService()


@router.post("/", response_model=HabitOut, status_code=status.HTTP_201_CREATED)
async def create_habit(
    payload: HabitCreate, user: TokenData = Depends(get_current_user)
):
    return await service.create_habit(payload, user.user_id)


@router.get("/progress", response_model=List[HabitProgress])
async def get_progress(
    user: TokenData = Depends(get_current_user),
) -> List[HabitProgress]:
    return await service.get_progress(user.user_id)


@router.get("/templates", response_model=List[TemplateHabitOut])
async def list_templates(
    user: TokenData = Depends(get_current_user),
) -> List[TemplateHabitOut]:
    return await service.list_templates()


@router.get("/{habit_id}")
async def get_habit(habit_id: str):
    habit = await Habit.get(habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@router.get("/", response_model=List[HabitOut])
async def list_habits(user: TokenData = Depends(get_current_user)) -> List[HabitOut]:
    return await service.list_habits(user)


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
    dailies = await DailyCompletions.find({"user_id": ObjectId(user.user_id)}).to_list()
    for daily_completion in dailies:
        completions_before = len(daily_completion.completions)
        daily_completion.completions = [
            c for c in daily_completion.completions if str(c.habit_id) != habit_id
        ]
        if len(daily_completion.completions) < completions_before:
            daily_completion.overall_percentage = (
                sum(c.percentage for c in daily_completion.completions)
                / len(daily_completion.completions)
                if daily_completion.completions
                else 0.0
            )
            daily_completion.day_completed = (
                all([c.completed for c in daily_completion.completions])
                if daily_completion.completions
                else False
            )
            await daily_completion.save()
    return None


@router.post(
    "/templates", response_model=TemplateHabitOut, status_code=status.HTTP_201_CREATED
)
async def create_template(
    payload: TemplateHabitCreate, user: TokenData = Depends(get_current_user)
) -> TemplateHabitOut:
    return await service.create_template(payload, user)


@router.patch("/templates/{template_id}", response_model=TemplateHabitOut)
async def update_template(
    template_id: str,
    payload: TemplateHabitUpdate,
    user: TokenData = Depends(get_current_user),
) -> TemplateHabitOut:
    return await service.update_template(template_id, payload, user)


@router.delete("/templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(
    template_id: str, user: TokenData = Depends(get_current_user)
):
    await service.delete_template(template_id, user)
    return None
