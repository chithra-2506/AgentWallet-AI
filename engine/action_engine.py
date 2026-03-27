# engine/action_engine.py

def take_action(decision, data):
    action = decision.get("action")
    conflict = decision.get("conflict", False)

    income = data.get("income", 0)
    expense = data.get("expense", 0)

    savings = income - expense

    response = {
        "message": "",
        "severity": "info",
        "recommendation": "",
        "auto_block": False
    }

    # Restrict case (highest severity)
    if action == "restrict":
        response["message"] = "⚠️ High Risk Spending Detected"
        response["severity"] = "error"
        response["recommendation"] = "This expense is too high compared to your income. Avoid this purchase."
        
        # Simulate blocking behavior
        if expense > income * 0.5:
            response["auto_block"] = True

    # Invest case
    elif action == "invest":
        invest_amount = int(savings * 0.5) if savings > 0 else 0

        response["message"] = "📈 Investment Opportunity Identified"
        response["severity"] = "success"
        response["recommendation"] = f"Consider investing around ₹{invest_amount} instead of spending."

    # Allow case
    elif action == "allow":
        response["message"] = "✅ Safe to Proceed"
        response["severity"] = "success"
        response["recommendation"] = "This expense is within your safe spending range."

    # Avoid case
    elif action == "avoid":
        response["message"] = "⚖️ Caution Advised"
        response["severity"] = "warning"
        response["recommendation"] = "This purchase may not be the best decision right now."

    # Hold case
    else:
        response["message"] = "ℹ️ Neutral Decision"
        response["severity"] = "info"
        response["recommendation"] = "Consider reviewing your finances before proceeding."

    # Conflict handling enhancement
    if conflict:
        response["message"] += " (Agents Disagree)"
        response["recommendation"] += " Multiple financial perspectives detected. Decide carefully."

    return response
