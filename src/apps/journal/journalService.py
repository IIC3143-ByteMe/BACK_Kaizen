from datetime import datetime
from typing import List, Optional
from apps.journal.journalDBRepository import JournalDBRepository
from models.models import Journal, JournalQuestion
from schemas.journal import JournalEntryCreate, JournalEntryOut, JournalQuestionOut
from schemas.roles import TokenData
from utils.gemini_util import get_gemini_model


class JournalService:
    def __init__(self):
        self.repo = JournalDBRepository()

    async def create_journal(self, user: TokenData) -> Journal:
        user_id = user.user_id
        return await self.repo.create_journal(user_id)

    async def get_journal(self, user: TokenData) -> Optional[Journal]:
        journal = await self.repo.get_journal_by_user_id(user.user_id)

        return journal

    async def get_or_create_journal(self, user: TokenData) -> Journal:
        journal = await self.get_journal(user)
        if not journal:
            journal = await self.create_journal(user)
        return journal

    async def create_journal_entry(
        self, payload: JournalEntryCreate, user: TokenData
    ) -> JournalEntryOut:
        journal = await self.get_or_create_journal(user)

        entry_data = payload.model_dump()
        entry = await self.repo.add_entry_to_journal(journal.id, entry_data)

        return JournalEntryOut.model_validate(entry.model_dump())

    async def get_journal_entries(self, user: TokenData) -> List[JournalEntryOut]:
        journal = await self.get_journal(user)
        if not journal:
            return []

        return [JournalEntryOut.model_validate(h.model_dump()) for h in journal.entries]

    async def get_journal_entry_by_date(
        self, user: TokenData, date: datetime
    ) -> Optional[JournalEntryOut]:
        entry = await self.repo.get_entry_by_date(user.user_id, date)
        if not entry:
            return None

        return JournalEntryOut.model_validate(entry.model_dump())

    async def create_daily_question(self) -> JournalQuestion:
        client = get_gemini_model()

        prompt = (
            "En el contexto de una aplicacion de habitos "
            "y desarrollo personal,"
            "tu tarea es generar una pregunta la cual sera "
            "considerada como la pregunta del dia."
            "Esta pregunta debe ser desde la perspectiva de"
            " la filosofia Kaizen (buscar algo que amas,"
            "que el mundo necesita, en lo que eres bueno y"
            " para lo que te puedan pagar). Considera que"
            "esta es una pregunta que deberan responder los"
            " usuarios para una seccion de journaling, asi que"
            "considera que sirva como introspeccion para que"
            " puedan conocerse mas y mejorar."
            "La frase debe ser simple, no muy larga, entendible,"
            " profunda y en español."
            "Responde UNICAMENTE con la pregunta, sin mas texto"
            " adicional"
        )

        question_data = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        ).text

        question = await self.repo.create_journal_question(question_data)

        return question

    async def get_or_create_daily_question(self) -> JournalQuestionOut:
        question = await self.repo.get_today_journal_question()
        if not question:
            question = await self.create_daily_question()

        return JournalQuestionOut.model_validate(question.model_dump())
