from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SettlementBase(BaseModel):
    amount: float


class SettlementCreate(SettlementBase):
    group_id: int
    from_user: int
    to_user: int
    evidence_url: Optional[str] = None


class SettlementResponse(SettlementBase):
    id: int
    group_id: int
    from_user: int
    to_user: int
    status: str
    evidence_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
