# ui/app.py

import streamlit as st
import pandas as pd
from datetime import datetime
from main import run_system

st.set_page_config(page_title="AgentWallet AI", layout="wide")

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "wallet" not in st.session_state:
    st.session_state.wallet = {
        "balance": 50000,
        "monthly_income": 50000,
        "spent": 0
    }

if "alerts" not in st.session_state:
    st.session_state.alerts = []

# ---------------- HEADER ----------------
st.title("💰 AgentWallet AI")
st.caption("Autonomous Financial Guardian • Real-Time Spending Intelligence")

# ---------------- SIDEBAR PROFILE ----------------
st.sidebar.header("👤 Financial Profile")

income = st.sidebar.number_input(
    "Monthly Income (₹)",
    value=st.session_state.wallet["monthly_income"]
)

st.session_state.wallet["monthly_income"] = income

st.sidebar.metric("💼 Balance", f"₹{st.session_state.wallet['balance']}")
st.sidebar.metric("💸 Spent", f"₹{st.session_state.wallet['spent']}")

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🛒 Marketplace",
    "💳 Payments",
    "📊 Insights",
    "🚨 Alerts"
])

# =========================================================
# 🛒 TAB 1: MARKETPLACE (Shopping Simulation)
# =========================================================
with tab1:

    st.subheader("🛍️ Smart Marketplace")

    products = [
        {"name": "iPhone 14", "price": 70000, "category": "electronics"},
        {"name": "Nike Shoes", "price": 3000, "category": "shopping"},
        {"name": "Laptop", "price": 55000, "category": "electronics"},
        {"name": "Headphones", "price": 2000, "category": "shopping"},
        {"name": "Watch", "price": 5000, "category": "shopping"},
        {"name": "Backpack", "price": 1500, "category": "shopping"},
    ]

    cols = st.columns(3)

    selected_product = None

    for i, product in enumerate(products):
        with cols[i % 3]:
            st.markdown(f"### {product['name']}")
            st.write(f"₹ {product['price']}")

            if st.button(f"Buy {product['name']}", key=product["name"]):
                selected_product = product

    if selected_product:
        st.subheader("⚡ Transaction Intercepted")

        data = {
            "income": income,
            "expense": selected_product["price"],
            "category": selected_product["category"],
            "history": st.session_state.history
        }

        result = run_system(data)

        decision = result["decision"]
        action = result["action"]

        # ---------------- AGENTS ----------------
        with st.expander("🤖 Agent Reasoning (Detailed)", expanded=True):
            for agent in result["agents"]:
                st.write(f"### {agent['agent'].capitalize()} Agent")
                st.write(agent["reason"])
                st.progress(agent["score"] / 10)

        # ---------------- ACTION ----------------
        st.subheader("🚨 Financial Decision")

        if action["severity"] == "error":
            st.error(action["message"])
        elif action["severity"] == "warning":
            st.warning(action["message"])
        else:
            st.success(action["message"])

        st.write(action["recommendation"])

        # ---------------- EXECUTION ----------------
        if not action.get("auto_block"):
            st.session_state.wallet["balance"] -= selected_product["price"]
            st.session_state.wallet["spent"] += selected_product["price"]

            st.session_state.history.append({
                "amount": selected_product["price"],
                "category": selected_product["category"],
                "time": str(datetime.now())
            })

        else:
            st.session_state.alerts.append("🚫 Blocked high-risk purchase")

# =========================================================
# 💳 TAB 2: PAYMENTS (Bills, Food, Travel)
# =========================================================
with tab2:

    st.subheader("💳 Daily Payments")

    col1, col2 = st.columns(2)

    with col1:
        food = st.number_input("🍔 Food / Dining (₹)", value=0)
        travel = st.number_input("✈️ Travel (₹)", value=0)

    with col2:
        bills = st.number_input("💡 Bills (₹)", value=0)
        entertainment = st.number_input("🎬 Entertainment (₹)", value=0)

    if st.button("Process Payments"):

        total = food + travel + bills + entertainment

        categories = [
            ("food", food),
            ("travel", travel),
            ("bills", bills),
            ("entertainment", entertainment)
        ]

        for cat, amt in categories:
            if amt > 0:
                data = {
                    "income": income,
                    "expense": amt,
                    "category": cat,
                    "history": st.session_state.history
                }

                result = run_system(data)
                action = result["action"]

                if not action.get("auto_block"):
                    st.session_state.wallet["balance"] -= amt
                    st.session_state.wallet["spent"] += amt

                    st.session_state.history.append({
                        "amount": amt,
                        "category": cat,
                        "time": str(datetime.now())
                    })
                else:
                    st.session_state.alerts.append(f"🚫 Blocked {cat} payment")

        st.success("Payments Processed")

# =========================================================
# 📊 TAB 3: INSIGHTS
# =========================================================
with tab3:

    st.subheader("📊 Financial Insights")

    if st.session_state.history:

        df = pd.DataFrame(st.session_state.history)

        st.write("### Spending Breakdown")
        st.bar_chart(df["category"].value_counts())

        total_spent = df["amount"].sum()
        st.metric("Total Spent", f"₹{total_spent}")

        # Behavior analysis
        if total_spent > income * 0.7:
            st.error("⚠️ You are overspending this month")
        elif total_spent > income * 0.4:
            st.warning("⚠️ Moderate spending detected")
        else:
            st.success("✅ Healthy spending habits")

    else:
        st.info("No data available")

# =========================================================
# 🚨 TAB 4: ALERTS
# =========================================================
with tab4:

    st.subheader("🚨 System Alerts")

    if st.session_state.alerts:
        for alert in st.session_state.alerts:
            st.warning(alert)
    else:
        st.success("No alerts")

# ---------------- FOOTER ----------------
st.divider()
st.caption("AgentWallet AI • Autonomous Financial Decision System")
