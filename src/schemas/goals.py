from pydantic import (
    BaseModel,
)


class Goal(BaseModel):
    period: str # daily
    type: str # check, sum, slide
    target: int 
    unit: str
