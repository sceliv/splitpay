from pydantic import BaseModel
from typing import List


class CompensationResult(BaseModel):
    payer_id: int
    receiver_id: int
    amount: float

    class Config:
        from_attributes = True
