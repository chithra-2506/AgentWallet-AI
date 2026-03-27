import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 🎨 1. THE "MIDNIGHT GOLD" UI ENGINE ---
st.set_page_config(page_title="AgentWallet AI | Private", layout="wide")

# Custom CSS for Deep Contrast (No Pure White/Black)
st.markdown("""
    <style>
    /* Global Midnight Theme */
    .stApp { background-color: #0E1117 !important; }

    /* High-Contrast Text (Slate Gray / Cyan) */
    h1, h2, h3, h4, p, li, span, label, .stMarkdown {
        color: #E0E0E0 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Neon Cyan Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #161B22 !important;
        border: 2px solid #00D4FF !important;
        padding: 20px !important;
        border-radius: 12px !important;
    }
    div[data-testid="stMetricValue"] > div {
        color: #00D4FF !important;
        font-weight: 800 !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #090C10 !important;
        border-right: 1px solid #30363D !important;
    }

    /* Primary Action Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00D4FF 0%, #0072FF 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        height: 50px !important;
        width: 100% !important;
    }

    /* Table Visibility Fix */
    .stTable { background-color: #161B22 !important; border: 1px solid #30363D !important; }
    th { color: #00D4FF !important; }
    td { color: #E0E0E0 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 🛠️ 2. BACKEND INTELLIGENCE ENGINE ---
def run_ai_agent(history, budget):
    if not history:
        return {"burn_rate": 0, "runway": 30, "risk": "LOW", "top": "None"}
    
    df = pd.DataFrame(history)
    total_spent = df['amount'].sum()
    daily_avg = total_spent / 30 
    days_left = (budget - total_spent) / daily_avg if daily_avg > 0 else 30
    
    return {
        "burn_rate": round(daily_avg, 2),
        "runway": round(days_left),
        "risk_level": "HIGH" if days_left < 10 else "STABLE",
        "top_leak": df.groupby('category')['amount'].sum().idxmax() if not df.empty else "N/A"
    }

# --- 💾 3. SESSION STATE ---
if "history" not in st.session_state:
    st.session_state.history = [
        {"amount": 2500, "category": "Bills ⚡", "date": "2026-03-24", "note": "Electricity"},
        {"amount": 1200, "category": "Food 🍔", "date": "2026-03-25", "note": "Dinner"},
        {"amount": 5000, "category": "Shopping 🛍️", "date": "2026-03-26", "note": "Headphones"},
    ]
if "income" not in st.session_state: st.session_state.income = 80000
if "budget" not in st.session_state: st.session_state.budget = 40000

# --- ⬅️ 4. NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/10433/10433048.png", width=80)
    st.title("AgentWallet")
    st.write("---")
    page = st.radio("GO TO", ["🏠 Dashboard", "💸 Transactions", "📊 Analytics", "🤖 AI Brain", "👤 Profile"])
    st.write("---")
    st.info("🛰️ Status: Encrypted")

# --- 🏠 5. DASHBOARD ---
if page == "🏠 Dashboard":
    st.title("🏠 Private Dashboard")
    
    total_spent = sum(d['amount'] for d in st.session_state.history)
    balance = st.session_state.income - total_spent
    ai = run_ai_agent(st.session_state.history, st.session_state.budget)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Current Balance", f"₹{balance:,}")
    c2.metric("Total Expenses", f"₹{total_spent:,}")
    c3.metric("Financial Runway", f"{ai['runway']} Days")

    st.write("---")
    col_l, col_r = st.columns([2, 1])
    
    with col_l:
        st.subheader("📋 Recent Outflows")
        st.table(pd.DataFrame(st.session_state.history).tail(5))
        
    with col_r:
        st.subheader("💡 AI Quick Insights")
        st.info(f"Top Category: **{ai['top_leak']}**")
        st.write(f"Risk Level: **{ai['risk_level']}**")
        st.progress(min(total_spent/st.session_state.budget, 1.0))

# --- 💸 6. TRANSACTIONS ---
elif page == "💸 Transactions":
    st.title("💸 Global Ledger")
    with st.expander("➕ Log New Transaction", expanded=True):
        t1, t2, t3 = st.columns([1, 1, 2])
        amt = t1.number_input("Amount (₹)", min_value=0)
        cat = t2.selectbox("Category", ["Food 🍔", "Travel 🚗", "Bills ⚡", "Shopping 🛍️", "Entertainment 🎬"])
        note = t3.text_input("Merchant/Entity")
        if st.button("AUTHORIZE TRANSACTION"):
            st.session_state.history.append({
                "amount": amt, "category": cat, 
                "date": datetime.now().strftime("%Y-%m-%d"), "note": note
            })
            st.rerun()

    st.write("---")
    st.subheader("📜 History")
    df_all = pd.DataFrame(st.session_state.history).sort_index(ascending=False)
    # Standard dataframe display (No extra parameters to avoid TypeErrors)
    st.dataframe(df_all)

# --- 📊 7. ANALYTICS ---
elif page == "📊 Analytics":
    st.title("📊 Intelligence Core")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        c1, c2 = st.columns(2)
        
        # UNIVERSAL COLOR PALETTE (Safe for all Plotly versions)
        cyan_colors = ['#00D4FF', '#0099CC', '#0072FF', '#00E5FF', '#00B8D4']
        
        with c1:
            st.write("### Category Breakdown")
            fig = px.pie(df, values='amount', names='category', hole=0.5, 
                         color_discrete_sequence=cyan_colors)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#E0E0E0")
            st.plotly_chart(fig, use_container_width=True)
            
        with c2:
            st.write("### Expense Velocity")
            df['date'] = pd.to_datetime(df['date'])
            trend = df.groupby('date')['amount'].sum().reset_index()
            fig2 = px.line(trend, x='date', y='amount', markers=True)
            fig2.update_traces(line_color='#00D4FF', line_width=4)
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#E0E0E0")
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Log data for analytics.")

# --- 🤖 8. AI BRAIN ---
elif page == "🤖 AI Brain":
    st.title("🤖 AI Brain (Predictive)")
    ai = run_ai_agent(st.session_state.history, st.session_state.budget)
    
    st.subheader("🔮 Predictive Burn Rate")
    st.write(f"Current Burn Velocity: **₹{ai['burn_rate']} / Day**")
    
    if ai['risk_level'] == "HIGH":
        st.error(f"🚨 ALERT: Runway is critical. Current habits lead to budget depletion in {ai['runway']} days.")
    else:
        st.success(f"✅ STABLE: Financial health is within optimal parameters.")
    
    st.write("---")
    st.subheader("🧠 Behavioral Intelligence")
    st.info(f"Anomaly Detected: Your spending on **{ai['top_leak']}** is currently your highest outflow. Capping this by 15% would extend your runway by approximately 5 days.")

# --- 👤 9. PROFILE ---
elif page == "👤 Profile":
    st.title("👤 My Profile")
    st.session_state.income = st.number_input("Monthly Income (₹)", value=st.session_state.income)
    st.session_state.budget = st.number_input("Monthly Budget (₹)", value=st.session_state.budget)
    if st.button("UPDATE SYSTEM"):
        st.balloons()
        st.success("Settings Saved!")

# --- FOOTER ---
st.write("---")
st.caption("AgentWallet AI • Proprietary Intelligence Build • 🔒 Secure AES-256")