import pandas as pd
import streamlit as st
import requests

def get_ai_insights(history, budget):
    if not history:
        return {"status": "No Data", "advice": "Start adding transactions to enable AI insights."}
    
    # --- 1. THE MATH LOGIC (Your existing code) ---
    df = pd.DataFrame(history)
    df['time'] = pd.to_datetime(df['time'])
    total_spent = df['amount'].sum()
    
    late_night_spend = df[df['time'].dt.hour > 20]['amount'].sum()
    top_cat = df.groupby('category')['amount'].sum().idxmax()
    
    insights = {
        "burn_rate": total_spent / 30,
        "runway": (budget - total_spent) / (total_spent / len(df)) if total_spent > 0 else 30,
        "patterns": [],
        "advice": [],
        "llm_response": ""
    }
    
    if late_night_spend > (total_spent * 0.3):
        insights["patterns"].append("⚠️ High Night Spending: 30%+ of expenses occur after 8 PM.")
    
    # --- 2. THE AI BRAIN (The New Part) ---
    try:
        # Pulling the key safely from Streamlit Secrets
        API_KEY = st.secrets["ai_engine"]["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"]
        
        prompt = f"""
        User Budget: ₹{budget}
        Total Spent: ₹{total_spent}
        Top Category: {top_cat}
        Late Night Spending: ₹{late_night_spend}
        
        Give 2 professional, short financial tips for this user. 
        Focus on their {top_cat} spending.
        """

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "google/gemini-2.0-flash-lite-001", 
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        insights["llm_response"] = response.json()["choices"][0]["message"]["content"]
    except Exception:
        insights["llm_response"] = "AI Advisor: Focus on reducing non-essential shopping to save 15% more this month."

    return insights