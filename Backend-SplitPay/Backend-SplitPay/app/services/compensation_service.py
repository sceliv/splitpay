from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.models.group_member import GroupMember
from app.utils.math_helpers import round_currency


def calculate_compensation(db: Session, group_id: int) -> list[dict]:
    """
    Calcula quién debe a quién dentro de un grupo.

    Devuelve una lista de dicts con las claves:
    - payer_id: usuario que debe pagar
    - receiver_id: usuario que debe recibir
    - amount: monto a pagar

    Esta estructura está alineada con el schema CompensationResult.
    """
    expenses = db.query(Expense).filter(Expense.group_id == group_id).all()
    members = db.query(GroupMember).filter(GroupMember.group_id == group_id).all()

    if not members:
        return []

    total = sum(e.amount for e in expenses)
    per_person = total / len(members)

    balances: dict[int, float] = {}

    for m in members:
        paid = sum(e.amount for e in expenses if e.user_id == m.user_id)
        balances[m.user_id] = paid - per_person

    debtors = [u for u in balances if balances[u] < 0]
    creditors = [u for u in balances if balances[u] > 0]

    debtors.sort(key=lambda x: balances[x])
    creditors.sort(key=lambda x: balances[x], reverse=True)

    result: list[dict] = []

    i = 0
    j = 0

    while i < len(debtors) and j < len(creditors):
        d = debtors[i]
        c = creditors[j]

        amount = min(-balances[d], balances[c])

        result.append(
            {
                "payer_id": d,
                "receiver_id": c,
                "amount": round_currency(amount),
            }
        )

        balances[d] += amount
        balances[c] -= amount

        if balances[d] == 0:
            i += 1
        if balances[c] == 0:
            j += 1

    return result
