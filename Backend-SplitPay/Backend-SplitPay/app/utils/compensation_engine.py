def calculate_balances(expenses, members):
    """
    Calcula el saldo de cada usuario.
    expenses: lista de objetos Expense
    members: lista de objetos GroupMember
    """

    total = sum(e.amount for e in expenses)
    n = len(members)
    if n == 0:
        return {}

    aporte_equivalente = total / n
    balances = {}

    # Inicializar todos en 0
    for m in members:
        balances[m.user_id] = 0

    # Sumar lo que pagó cada uno
    for e in expenses:
        balances[e.user_id] += e.amount

    # Restar aporte equivalente
    for uid in balances:
        balances[uid] -= aporte_equivalente

    return balances


def generate_compensation(balances):
    """
    Genera la lista mínima de pagos para saldar deudas.
    balances: { user_id: saldo }
    """

    debtors = []   # saldo < 0 (deben)
    creditors = [] # saldo > 0 (tienen a favor)

    for uid, balance in balances.items():
        if balance < 0:
            debtors.append([uid, -balance])  # convertir a positivo
        elif balance > 0:
            creditors.append([uid, balance])

    result = []

    i = 0
    j = 0

    while i < len(debtors) and j < len(creditors):
        debtor_id, debt_amount = debtors[i]
        creditor_id, credit_amount = creditors[j]

        monto = min(debt_amount, credit_amount)

        result.append({
            "from_user": debtor_id,
            "to_user": creditor_id,
            "amount": round(monto, 2)
        })

        # Restar lo pagado
        debtors[i][1] -= monto
        creditors[j][1] -= monto

        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    return result
