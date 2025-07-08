from bson import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException
from models.models import DailyCompletions, Habit, UpdateProgressInput
from datetime import date, datetime

from schemas.roles import TokenData
from utils.dependencies import get_current_user

router = APIRouter()


@router.post("/daily-completions/")
async def get_or_create_daily_completion(
    date: date = Body(...),
    user: TokenData = Depends(get_current_user),
):
    user_id = user.user_id
    existing = await DailyCompletions.find_one(
        {"user_id": ObjectId(user_id), "date": date}
    )
    if existing:
        return existing

    weekday = date.strftime("%a")

    habits = await Habit.find(
        {"owner_id": ObjectId(user_id), "task_days": weekday}
    ).to_list()

    if not habits:
        return []

    completions = []
    for h in habits:
        completions.append(
            {
                "habit_id": h.id,
                "title": h.title,
                "goal": h.goal,
                "progress": 0.0,
                "percentage": 0.0,
                "completed": False,
            }
        )

    overall_percentage = (
        sum(c["percentage"] for c in completions) / len(completions)
        if completions
        else 0.0
    )

    dc = DailyCompletions(
        user_id=ObjectId(user_id),
        date=date,
        completions=completions,
        overall_percentage=overall_percentage,
        day_completed=False,
    )
    await dc.insert()
    return dc


@router.patch("/daily-completions/update-progress")
async def update_completion_progress(
    data: UpdateProgressInput = Body(...),
    user: TokenData = Depends(get_current_user),
):
    user_id = user.user_id

    dc = await DailyCompletions.find_one(
        {"user_id": ObjectId(user_id), "date": data.date}
    )
    if not dc:
        raise HTTPException(status_code=404, detail="DailyCompletions not found")

    found = False
    for c in dc.completions:
        if str(c.habit_id) == data.habit_id:
            found = True
            c.progress = float(data.progress)
            goal = c.goal
            target = 1
            if isinstance(goal, dict):
                target = goal.get("target", 1) or 1
            elif hasattr(goal, "target"):
                target = getattr(goal, "target", 1) or 1
            c.percentage = float(c.progress) / float(target)
            c.completed = c.percentage >= 1.0
            break

    if not found:
        from models.models import Habit

        habit = await Habit.find_one(
            {"_id": ObjectId(data.habit_id), "owner_id": ObjectId(user_id)}
        )
        if not habit:
            raise HTTPException(status_code=404, detail="Habit not found")

        goal = habit.goal
        target = goal.target if hasattr(goal, "target") else 1
        percentage = float(data.progress) / float(target) if target else 0.0
        completion = type(dc.completions[0])(
            habit_id=habit.id,
            title=habit.title,
            goal=goal,
            progress=float(data.progress),
            percentage=percentage,
            completed=percentage >= 1.0,
        )
        dc.completions.append(completion)

    dc.overall_percentage = sum([c.percentage for c in dc.completions]) / len(
        dc.completions
    )
    dc.day_completed = all([c.completed for c in dc.completions])
    await dc.save()
    # await update_calendar_day_stats(user_id, dc.date, dc.completions)

    return dc


@router.get("/daily-completions/{day}")
async def get_daily_completion(
    day: str,
    user: TokenData = Depends(get_current_user),
):
    dt = datetime.strptime(day, "%Y-%m-%d").date()
    obj = await DailyCompletions.find_one(
        DailyCompletions.user_id == ObjectId(user.user_id), DailyCompletions.date == dt
    )
    if not obj:
        raise HTTPException(
            status_code=404, detail="No daily completion found for this user and date"
        )
    return obj