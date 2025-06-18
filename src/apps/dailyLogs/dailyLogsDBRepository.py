from typing import List, Optional
from models.models import DailyHabitLog


class DailyLogsDBRepository:
    async def create_log(self, data: dict) -> DailyHabitLog:
        log = DailyHabitLog(**data)
        await log.insert()
        return log

    async def list_user_logs(self, user_id: str) -> List[DailyHabitLog]:
        return await DailyHabitLog.find(
            DailyHabitLog.user_id == user_id
        ).to_list()

    async def get_log(self, log_id: str) -> Optional[DailyHabitLog]:
        return await DailyHabitLog.get(log_id)

    async def save_log(self, log: DailyHabitLog) -> DailyHabitLog:
        await log.save()
        return log

    async def delete_log(self, log: DailyHabitLog) -> None:
        await log.delete()