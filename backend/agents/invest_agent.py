# agents/invest_agent.py

def evaluate(data):
    income = data.get("income", 0)
    expense = data.get("expense", 0)
    history = data.get("history", [])

    if income <= 0:
        return {
            "agent": "invest",
            "score": 5,
            "reason": "No income data available",
            "action": "hold"
        }

    savings = income - expense

    # Calculate total past spending
    total_spent = sum(tx["amount"] for tx in history)

    # Savings ratio
    savings_ratio = savings / income if income else 0

    score = 5
    reasons = []

    # Rule 1: High savings → invest
    if savings_ratio > 0.4:
        score += 3
        reasons.append("Strong savings ratio")

    elif savings_ratio > 0.2:
        score += 1
        reasons.append("Moderate savings available")

    else:
        score -= 2
        reasons.append("Low savings")

    # Rule 2: Heavy spending history → push investment
    if total_spent > income * 0.7:
        score += 2
        reasons.append("High past spending, better to invest now")

    # Rule 3: Very low savings → avoid investing
    if savings < 1000:
        score -= 2
        reasons.append("Not enough surplus for safe investment")

    # Cap score
    score = max(1, min(score, 10))

    action = "invest" if score >= 7 else "hold"

    return {
        "agent": "invest",
        "score": score,
        "reason": " | ".join(reasons) if reasons else "Neutral investment decision",
        "action": action
    }
