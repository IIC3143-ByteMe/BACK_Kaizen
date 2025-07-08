from datetime import datetime
from typing import Optional

from bson import ObjectId

from models.models import Journal, JournalEntry, JournalQuestion


class JournalDBRepository:
    async def create_journal_question(self, question: str) -> JournalQuestion:
        today = datetime.combine(datetime.today().date(), datetime.min.time())
        journal_question_data = {
            "date": today,
            "question": question,
        }

        question = JournalQuestion(**journal_question_data)
        await question.insert()
        return question

    async def get_today_journal_question(self) -> Optional[JournalQuestion]:
        today = datetime.combine(datetime.today().date(), datetime.min.time())
        return await JournalQuestion.find(JournalQuestion.date == today).first_or_none()

    async def create_journal(self, user_id: str) -> Journal:
        journal_data = {
            "user_id": ObjectId(user_id),
        }

        journal = Journal(**journal_data)
        await journal.insert()
        return journal

    async def get_journal_by_user_id(self, user_id: str) -> Optional[Journal]:
        journal = await Journal.find_one(Journal.user_id == ObjectId(user_id))
        return journal

    async def get_journal(self, id: str) -> Journal:
        journal = await Journal.get(id)
        return journal

    async def add_entry_to_journal(
        self, journal_id: str, entry_data: dict
    ) -> JournalEntry:
        today = datetime.combine(datetime.today().date(), datetime.min.time())
        entry_data["date"] = today
        entry = JournalEntry(**entry_data)

        journal = await self.get_journal(journal_id)
        journal.entries.append(entry)
        await journal.save()

        return entry

    async def get_entry_by_date(
        self, user_id: str, date: datetime
    ) -> Optional[JournalEntry]:
        journal = await self.get_journal_by_user_id(user_id)
        if not journal:
            return None

        target = date.date()

        for entry in journal.entries:
            if entry.date == target:
                return entry

        return None
