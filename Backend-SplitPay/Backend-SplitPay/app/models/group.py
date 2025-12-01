from sqlalchemy import Column, Integer, String
from app.database import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    creator_id = Column(Integer, nullable=False)

    type = Column(String(50), nullable=True)
    currency = Column(String(10), nullable=True)
