from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ExpenseBase(BaseModel):
    amount: float
    description: str


class ExpenseCreate(ExpenseBase):
    user_id: int
    group_id: int


class ExpenseResponse(ExpenseBase):
    id: int
    user_id: int
    group_id: int
    created_at: datetime

    class Config:
        from_attributes = True
