# agents/save_agent.py

def evaluate(data):
    income = data.get("income", 0)
    expense = data.get("expense", 0)
    category = data.get("category", "other")
    history = data.get("history", [])

    if income <= 0:
        return {
            "agent": "save",
            "score": 5,
            "reason": "No income data available",
            "action": "hold"
        }

    # Current ratio
    ratio = expense / income

    # Historical category spending
    category_spend = sum(
        tx["amount"] for tx in history if tx["category"] == category
    )

    category_ratio = category_spend / income if income else 0

    score = 5
    reasons = []

    # Rule 1: High single expense
    if ratio > 0.4:
        score += 3
        reasons.append("High single expense compared to income")

    # Rule 2: Category overuse
    if category_ratio > 0.3:
        score += 2
        reasons.append(f"Overspending in {category} category")

    # Rule 3: Too many recent transactions
    if len(history) > 5:
        score += 1
        reasons.append("Frequent recent spending detected")

    # Cap score
    score = min(score, 10)

    action = "restrict" if score >= 7 else "allow"

    return {
        "agent": "save",
        "score": score,
        "reason": " | ".join(reasons) if reasons else "Spending within safe limits",
        "action": action
    }
