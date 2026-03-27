import pandas as pd
from datetime import datetime, timedelta

def generate_insights(history, income):

    if not history:
        return {}

    df = pd.DataFrame(history)

    total_spent = df["amount"].sum()

    # Burn rate (daily average)
    days = max(len(df), 1)
    burn_rate = total_spent / days

    # Days left prediction
    remaining_money = income - total_spent
    days_left = int(remaining_money / burn_rate) if burn_rate > 0 else 0

    # Category analysis
    category_spend = df.groupby("category")["amount"].sum().to_dict()

    top_category = max(category_spend, key=category_spend.get)

    # Overspending detection
    overspending = total_spent > income * 0.7

    # Suggestions
    suggestions = []

    if overspending:
        suggestions.append("You are overspending. Reduce unnecessary expenses.")

    if top_category == "food":
        suggestions.append("Reduce food delivery expenses by 20%")

    if burn_rate > income / 30:
        suggestions.append("Your daily spending is too high")

    return {
        "total_spent": total_spent,
        "burn_rate": burn_rate,
        "days_left": days_left,
        "top_category": top_category,
        "category_spend": category_spend,
        "overspending": overspending,
        "suggestions": suggestions
    }
