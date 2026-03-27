def check_budget(history, budgets):

    alerts = []

    category_totals = {}

    for tx in history:
        cat = tx["category"]
        category_totals[cat] = category_totals.get(cat, 0) + tx["amount"]

    for cat, limit in budgets.items():
        if cat in category_totals and category_totals[cat] > limit:
            alerts.append(f"⚠️ Budget exceeded for {cat}")

    return alerts
