from pydantic import BaseModel
from typing import List, Optional


class GroupBase(BaseModel):
    name: str
    type: Optional[str] = None
    currency: Optional[str] = None


class GroupCreate(GroupBase):
    members: List[str] = []  # lista de emails


class AddMemberSchema(BaseModel):
    user_id: int
    role: Optional[str] = "member"


class AddMemberByEmailSchema(BaseModel):
    email: str
    role: Optional[str] = "member"


class GroupMember(BaseModel):
    user_id: int
    role: str

    class Config:
        from_attributes = True


class GroupResponse(GroupBase):
    id: int
    members: List[GroupMember] = []

    class Config:
        from_attributes = True
