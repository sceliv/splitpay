from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import create_user, get_user
from app.core.exceptions import not_found

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse)
def create_new_user(user_data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    return create_user(db, user_data)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    result = get_user(db, user_id)
    if result is None:
        not_found("User not found")
    return result
