from bson import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException
from models.models import DailyCompletions, Habit, UpdateProgressInput, User
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
    just_completed = False

    for c in dc.completions:
        if str(c.habit_id) == data.habit_id:
            found = True
            prev_completed = c.completed
            c.progress = float(data.progress)
            goal = c.goal
            target = 1
            if isinstance(goal, dict):
                target = goal.get("target", 1) or 1
            elif hasattr(goal, "target"):
                target = getattr(goal, "target", 1) or 1
            c.percentage = float(c.progress) / float(target)
            c.completed = c.percentage >= 1.0
            if not prev_completed and c.completed:
                just_completed = True
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
        completed = percentage >= 1.0
        completion = type(dc.completions[0])(
            habit_id=habit.id,
            title=habit.title,
            goal=goal,
            progress=float(data.progress),
            percentage=percentage,
            completed=completed,
        )
        dc.completions.append(completion)
        if completed:
            just_completed = True

    dc.overall_percentage = sum([c.percentage for c in dc.completions]) / len(
        dc.completions
    )
    dc.day_completed = all([c.completed for c in dc.completions])
    await dc.save()

    if just_completed:
        user_doc = await User.get(ObjectId(user.user_id))
        if user_doc and (
            user_doc.last_timestamp is None or user_doc.last_timestamp != date.today()
        ):
            user_doc.update_streak()
            await user_doc.save()

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


@router.delete("/daily-completions/{id}", status_code=204)
async def delete_daily_completion(id: str, user: TokenData = Depends(get_current_user)):
    obj = await DailyCompletions.get(ObjectId(id))
    if obj and str(obj.user_id) == user.user_id:
        await obj.delete()
    return None


@router.get("/month-completions/{month}")
async def get_monthly_completion(
    month: str,
    user: TokenData = Depends(get_current_user),
):
    start = datetime.strptime(month, "%Y-%m")

    completions = await DailyCompletions.find_many(
        DailyCompletions.user_id == ObjectId(user.user_id)
    ).to_list()

    filtered = [
        c
        for c in completions
        if c.date.year == start.year and c.date.month == start.month
    ]

    return filtered
