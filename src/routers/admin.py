from typing import List
from fastapi import APIRouter, Depends, status
from schemas.schemas import HabitProgress, TokenData
from utils.dependencies import require_admin
from apps.admin.adminService import AdminService

router = APIRouter(prefix="/admin", tags=["admin"])
service = AdminService()

@router.get(
    "/user-progress/{user_id}",
    response_model=List[HabitProgress]
)
async def get_user_progress(
    user_id: str,
    admin: TokenData = Depends(require_admin)
) -> List[HabitProgress]:
    return await service.get_user_progress(user_id, admin)

@router.delete(
    "/habit/{habit_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def admin_delete_habit(
    habit_id: str,
    admin: TokenData = Depends(require_admin)
):
    await service.delete_habit(habit_id, admin)
    return None