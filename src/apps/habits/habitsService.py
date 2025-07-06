from typing import List
from apps.habits.habitsDBRepository import HabitsRepository
from schemas.habits import (
    HabitCreate,
    HabitUpdate,
    HabitOut,
    HabitProgress,
)
from schemas.templates import (
    TemplateCreate,
    TemplateUpdate,
    TemplateOut,
)
from fastapi import HTTPException


class HabitsService:
    def __init__(self):
        self.repo = HabitsRepository()

    async def create_habit(self, payload: HabitCreate, owner_id: str) -> HabitOut:
        data = payload.dict()
        data["owner_id"] = owner_id
        habit = await self.repo.create_habit(data)
        return HabitOut.from_orm(habit)

    async def list_habits(self, owner_id: str) -> List[HabitOut]:
        habits = await self.repo.list_user_habits(owner_id)
        return [HabitOut.from_orm(h) for h in habits]

    async def update_habit(
        self, habit_id: str, payload: HabitUpdate, actor
    ) -> HabitOut:
        habit = await self.repo.get_habit(habit_id)
        if not habit:
            raise HTTPException(status_code=404, detail="Hábito no encontrado")
        if habit.owner_id != actor.user_id and actor.role != "admin":
            raise HTTPException(status_code=403, detail="Permisos insuficientes")
        changes = payload.dict(exclude_unset=True)
        for k, v in changes.items():
            setattr(habit, k, v)
        updated = await self.repo.save_habit(habit)
        return HabitOut.from_orm(updated)

    async def delete_habit(self, habit_id: str) -> None:
        habit = await self.repo.get_habit(habit_id)
        if not habit:
            raise HTTPException(status_code=404, detail="Hábito no encontrado")
        await self.repo.delete_habit(habit)

    async def get_progress(self, owner_id: str) -> List[HabitProgress]:
        habits = await self.repo.list_user_habits(owner_id)
        result = []
        for h in habits:
            logs = await self.repo.get_logs(owner_id, str(h.id))
            total = len(logs)
            done = sum(1 for log in logs if log.completed)
            rate = (done / total * 100) if total else 0.0
            result.append(
                HabitProgress(
                    habit_id=str(h.id),
                    total_days=total,
                    completed_days=done,
                    completion_rate=rate,
                )
            )
        return result

    async def list_templates(self) -> List[TemplateOut]:
        tmpls = await self.repo.list_templates()
        return [TemplateOut.from_orm(t) for t in tmpls]

    async def create_template(self, payload: TemplateCreate, actor) -> TemplateOut:
        if actor.role != "admin":
            raise HTTPException(status_code=403, detail="Not authorized")
        tmpl = await self.repo.create_template(payload.dict())
        return TemplateOut.from_orm(tmpl)

    async def update_template(
        self, template_id: str, changes: TemplateUpdate, actor
    ) -> TemplateOut:
        if actor.role != "admin":
            raise HTTPException(status_code=403, detail="Not authorized")
        tmpl = await self.repo.get_template(template_id)
        if not tmpl:
            raise HTTPException(status_code=404, detail="Template not found")
        updated = await self.repo.update_template(
            tmpl, changes.dict(exclude_unset=True)
        )
        return TemplateOut.from_orm(updated)

    async def delete_template(self, template_id: str, actor) -> None:
        if actor.role != "admin":
            raise HTTPException(status_code=403, detail="Not authorized")
        tmpl = await self.repo.get_template(template_id)
        if not tmpl:
            raise HTTPException(status_code=404, detail="Template not found")
        await self.repo.delete_template(tmpl)
