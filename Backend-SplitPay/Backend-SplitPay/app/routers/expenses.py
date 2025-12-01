from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.expense_schema import ExpenseCreate, ExpenseResponse
from app.services.expense_service import create_expense, get_expenses_by_group

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/", response_model=ExpenseResponse)
def create_expense_route(expense_data: ExpenseCreate, db: Session = Depends(get_db)):
    return create_expense(db, expense_data)


@router.get("/group/{group_id}", response_model=list[ExpenseResponse])
def list_expenses_for_group(group_id: int, db: Session = Depends(get_db)):
    return get_expenses_by_group(db, group_id)
