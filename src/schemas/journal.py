from typing import List
from pydantic import BaseModel
from datetime import datetime


class JournalEntryCreate(BaseModel):
    entry: str


class JournalEntryOut(BaseModel):
    date: datetime
    entry: str


class JournalOut(BaseModel):
    user_id: str
    entries: List[JournalEntryOut]


class JournalQuestionOut(BaseModel):
    question: str
