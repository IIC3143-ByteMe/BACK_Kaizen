from pydantic import (
    BaseModel,
)


class Goal(BaseModel):
    period: str
    type: str
    target: int
    unit: str
