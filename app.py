
import streamlit as st

# Page setup
st.set_page_config(page_title="PropFirm Trading Calculator", layout="wide")

# Sidebar
st.sidebar.title("🎯 Prop Firm Settings")
prop_firm = st.sidebar.selectbox("Choose Prop Firm", ["FTMO", "FunderPro", "FundedNext", "FundingPips"])
account_type = st.sidebar.selectbox("Account Type", ["Normal", "Aggressive"])
phase = st.sidebar.selectbox("Phase", ["Phase 1", "Phase 2", "Funded"])

# Tabs
tabs = st.tabs(["📈 Forex Calculator", "🇮🇳 Indian Market", "🏢 Prop Firm Rules"])

# --- Forex Calculator Tab ---
with tabs[0]:
    st.header("📈 Forex Risk & Trade Calculator")

    col1, col2, col3 = st.columns(3)
    with col1:
        balance = st.number_input("Account Balance", value=5000.0)
    with col2:
        risk_percent = st.number_input("Risk % per Trade", value=1.0)
    with col3:
        sl_pips = st.number_input("Stop Loss (pips)", value=20.0)

    risk_amount = balance * (risk_percent / 100)
    pip_value = risk_amount / sl_pips if sl_pips else 0
    lot_size = pip_value / 10  # Approximation for most pairs

    st.success(f"🔢 Risk Amount: ${risk_amount:.2f} | Lot Size: {lot_size:.2f} lots")

    with st.expander("🧠 Smart Trade Evaluator"):
        entry = st.number_input("Entry Price", value=1.1000)
        stop_loss = st.number_input("Stop Loss Price", value=1.0980)
        take_profit = st.number_input("Take Profit Price", value=1.1060)

        sl_range = abs(entry - stop_loss)
        tp_range = abs(take_profit - entry)
        rr_ratio = tp_range / sl_range if sl_range else 0
        outcome = "✅ Trade has good RR" if rr_ratio >= 2 else "⚠️ Risky or low RR"

        st.write(f"📊 R:R Ratio: **{rr_ratio:.2f}** — {outcome}")

    with st.expander("📈 RR Tree Planner"):
        st.write("Visualize multiple TP levels:")
        for r in range(1, 6):
            profit = risk_amount * r
            st.write(f"{r}R ➜ Profit: ${profit:.2f}")

    with st.expander("🔥 Volatility-Based Lot Adjuster"):
        avg_spread = st.number_input("Average Spread (pips)", value=1.2)
        spread_multiplier = 1 + (avg_spread / 10)
        adjusted_lot = lot_size / spread_multiplier
        st.info(f"📉 Adjusted Lot Size (volatility-based): {adjusted_lot:.2f} lots")

# --- Indian Market Tab ---
with tabs[1]:
    st.header("🇮🇳 Indian Stocks & Indices")
    st.warning("Margin calculator for NSE stocks, Nifty, BankNifty coming soon!")

# --- Prop Firm Rules Tab ---
with tabs[2]:
    st.header("🏢 Prop Firm Rule Engine")

    rules = {
        "FTMO": {
            "Phase 1": {"daily_loss": 500, "max_loss": 1000, "target": 500},
            "Phase 2": {"daily_loss": 500, "max_loss": 1000, "target": 250},
            "Funded": {"daily_loss": 500, "max_loss": 1000, "target": "No Target"},
        },
        "FunderPro": {
            "Phase 1": {"daily_loss": 300, "max_loss": 600, "target": 600},
            "Phase 2": {"daily_loss": 300, "max_loss": 600, "target": 300},
            "Funded": {"daily_loss": 300, "max_loss": 600, "target": "No Target"},
        },
        "FundedNext": {
            "Phase 1": {"daily_loss": 360, "max_loss": 720, "target": 600},
            "Phase 2": {"daily_loss": 360, "max_loss": 720, "target": 300},
            "Funded": {"daily_loss": 360, "max_loss": 720, "target": "No Target"},
        },
        "FundingPips": {
            "Phase 1": {"daily_loss": 350, "max_loss": 700, "target": 700},
            "Phase 2": {"daily_loss": 350, "max_loss": 700, "target": 350},
            "Funded": {"daily_loss": 350, "max_loss": 700, "target": "No Target"},
        },
    }

    current_rules = rules[prop_firm][phase]
    st.subheader(f"{prop_firm} - {phase} Rules")
    st.metric("📉 Daily Loss Limit", f"${current_rules['daily_loss']}")
    st.metric("💥 Max Drawdown", f"${current_rules['max_loss']}")
    st.metric("🎯 Profit Target", f"${current_rules['target']}")
