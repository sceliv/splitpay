from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.schemas.expense_schema import ExpenseCreate


def create_expense(db: Session, data: ExpenseCreate):
    exp = Expense(
        group_id=data.group_id,
        user_id=data.user_id,
        amount=data.amount,
        description=data.description
    )
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp


def get_expenses_by_group(db: Session, group_id: int):
    return db.query(Expense).filter(Expense.group_id == group_id).all()
