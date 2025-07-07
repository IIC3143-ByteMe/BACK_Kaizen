from typing import List, Optional

from beanie import PydanticObjectId
from models.models import Habit, HabitTemplate


class HabitsRepository:
    async def create_habit(self, data: dict) -> Habit:
        habit = Habit(**data)
        await habit.insert()
        return habit

    async def list_user_habits(self, owner_id: str) -> List[Habit]:
        habits = await Habit.find(
            Habit.owner_id == PydanticObjectId(owner_id)
        ).to_list()
        return habits

    async def get_habit(self, habit_id: str) -> Optional[Habit]:
        return await Habit.get(habit_id)

    async def save_habit(self, habit: Habit) -> Habit:
        await habit.save()
        return habit

    async def delete_habit(self, habit: Habit) -> None:
        await habit.delete()

    async def list_templates(self) -> List[HabitTemplate]:
        return await HabitTemplate.find(HabitTemplate.published).to_list()

    async def create_template(self, data: dict) -> HabitTemplate:
        tmpl = HabitTemplate(**data)
        await tmpl.insert()
        return tmpl

    async def get_template(self, template_id: str) -> Optional[HabitTemplate]:
        return await HabitTemplate.get(template_id)

    async def update_template(
        self, tmpl: HabitTemplate, changes: dict
    ) -> HabitTemplate:
        await tmpl.set(changes)
        return tmpl

    async def delete_template(self, tmpl: HabitTemplate) -> None:
        await tmpl.delete()
