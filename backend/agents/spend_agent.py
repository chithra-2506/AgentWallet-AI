# agents/spend_agent.py

def evaluate(data):
    income = data.get("income", 0)
    expense = data.get("expense", 0)
    category = data.get("category", "other")
    history = data.get("history", [])

    if income <= 0:
        return {
            "agent": "spend",
            "score": 5,
            "reason": "No income data available",
            "action": "hold"
        }

    ratio = expense / income

    # Track diversity of spending (healthy behavior)
    categories_used = set(tx["category"] for tx in history)
    diversity_bonus = 1 if len(categories_used) > 3 else 0

    score = 5
    reasons = []

    # Rule 1: Affordable purchase
    if ratio < 0.25:
        score += 3
        reasons.append("Expense is affordable")

    elif ratio < 0.4:
        score += 1
        reasons.append("Expense is moderately affordable")

    else:
        score -= 2
        reasons.append("Expense is relatively high")

    # Rule 2: Encourage balanced lifestyle
    if category not in categories_used:
        score += 1
        reasons.append("New category purchase (balanced lifestyle)")

    # Rule 3: Diversity bonus
    score += diversity_bonus
    if diversity_bonus:
        reasons.append("Good spending diversity")

    # Cap score
    score = max(1, min(score, 10))

    action = "allow" if score >= 6 else "avoid"

    return {
        "agent": "spend",
        "score": score,
        "reason": " | ".join(reasons) if reasons else "Neutral spending decision",
        "action": action
    }
