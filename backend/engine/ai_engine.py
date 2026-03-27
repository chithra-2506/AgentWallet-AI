# backend/engine/ai_engine.py
import pandas as pd

def get_ai_insights(history, budget):
    if not history:
        return {"status": "No Data", "advice": "Start adding transactions to enable AI insights."}
    
    df = pd.DataFrame(history)
    df['time'] = pd.to_datetime(df['time'])
    total_spent = df['amount'].sum()
    
    # Logic: Pattern Detection
    late_night_spend = df[df['time'].dt.hour > 20]['amount'].sum()
    top_cat = df.groupby('category')['amount'].sum().idxmax()
    
    insights = {
        "burn_rate": total_spent / 30, # Simple monthly average
        "runway": (budget - total_spent) / (total_spent / len(df)) if total_spent > 0 else 30,
        "patterns": [],
        "advice": []
    }
    
    if late_night_spend > (total_spent * 0.3):
        insights["patterns"].append("⚠️ High Night Spending: 30%+ of expenses occur after 8 PM.")
    
    if total_spent > budget * 0.8:
        insights["advice"].append(f"🚨 Critical: You've used 80% of your budget. Reduce {top_cat} immediately.")
    else:
        insights["advice"].append(f"✅ On Track: Your current spending allows for ₹{round(budget - total_spent, 2)} in savings.")
        
    return insights