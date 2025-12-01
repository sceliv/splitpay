from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.compensation_service import calculate_compensation
from app.schemas.compensation_schema import CompensationResult

router = APIRouter(prefix="/compensation", tags=["Compensation"])

@router.get("/{group_id}", response_model=list[CompensationResult])
def compensation_route(group_id: int, db: Session = Depends(get_db)):
    return calculate_compensation(db, group_id)
