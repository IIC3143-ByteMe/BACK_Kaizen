from datetime import datetime
from fastapi import APIRouter, Depends, status
from typing import List, Optional
from apps.journal.journalService import JournalService
from schemas.journal import JournalEntryCreate, JournalEntryOut, JournalQuestionOut
from schemas.roles import TokenData
from utils.dependencies import get_current_user

router = APIRouter(prefix="/journal", tags=["journal"])
service = JournalService()


@router.post(
    "/entry", response_model=JournalEntryOut, status_code=status.HTTP_201_CREATED
)
async def create_journal_entry(
    payload: JournalEntryCreate, user: TokenData = Depends(get_current_user)
):
    return await service.create_journal_entry(payload, user)


@router.get(
    "/entry/{day}",
    response_model=Optional[JournalEntryOut],
    status_code=status.HTTP_201_CREATED,
)
async def get_entry(day: str, user: TokenData = Depends(get_current_user)):
    dt = datetime.strptime(day, "%Y-%m-%d").date()
    consult_day = datetime.combine(dt, datetime.min.time())
    return await service.get_journal_entry_by_date(user, consult_day)


@router.get(
    "/entries",
    response_model=List[JournalEntryOut],
    status_code=status.HTTP_201_CREATED,
)
async def get_entries(user: TokenData = Depends(get_current_user)):
    return await service.get_journal_entries(user)


@router.get(
    "/question", response_model=JournalQuestionOut, status_code=status.HTTP_201_CREATED
)
async def get_question(user: TokenData = Depends(get_current_user)):
    return await service.get_or_create_daily_question()
