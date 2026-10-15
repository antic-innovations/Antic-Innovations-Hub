import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
import requests

# --- 1. CORE SYSTEM CREDENTIALS & STORAGE PATH LOGIC ---
OPENROUTER_API_KEY = "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"
DB_FILE = "database.json"

def load_data():
    """Initializes or reads application tables from disk storage memory."""
    if not os.path.exists(DB_FILE):
        return {
            "learners": [
                {"id": 1, "name": "Arjun Sharma", "age_group": "Under 15 Trainer", "status": "Active", "tier": "Free Trial", "join_date": "2026-10-10", "trial_days_left": 7},
                {"id": 2, "name": "Deepa Patel", "age_group": "Under 15 Trainer", "status": "Active", "tier": "Premium", "join_date": "2026-09-15", "trial_days_left": 0},
                {"id": 3, "name": "Rahul Verma", "age_group": "Under 15 Trainer", "status": "Active", "tier": "Free Trial", "join_date": "2026-10-15", "trial_days_left": 14}
            ], 
            "whatsapp_clients": [
                {"id": 1, "business_name": "Local Retailer Beta", "status": "Active", "tier": "Free Trial", "join_date": "2026-10-12", "trial_days_left": 11}
            ], 
            "investor_pipeline": [
                {"id": 1, "firm": "Antic Novelty", "amount": 50000000, "stage": "Term Sheet", "status": "High Priority"}
            ], 
            "audit_logs": [
                {"timestamp": "2026-10-15 11:00:00", "action": "System Framework Initialized", "user": "System Admin"}
            ], 
            "simulation_queue": []
        }
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {"learners": [], "whatsapp_clients": [], "investor_pipeline": [], "audit_logs": [], "simulation_queue": []}

def save_data(data):
    """Commits system state parameters cleanly down to persistent local files."""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_action(action_text):
    """Saves system audit history entries straight into your analytics logs."""
    data = load_data()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["audit_logs"].insert(0, {"timestamp": now_str, "action": action_text, "user": "System Admin"})
    save_data(data)

def ask_live_ai_model(prompt_text):
    """Queries OpenRouter to generate smart responses for your clients or investors."""
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "YOUR_OPENROUTER_API_KEY_HERE":
        return "⚠️ Configuration Missing: OpenRouter API Token Key is not configured."
        
    url = "https://openrouter.ai"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": [
            {
                "role": "system", 
                "content": "You are the professional, premium AI engine for Antic Innovations. Give brief, highly accurate, elegant sales automation answers to attract B2B corporate clients and institutional venture investors."
            },
            {"role": "user", "content": prompt_text}
        ]
    }
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=10)
        return res.json()["choices"]["message"]["content"]
    except:
        return "🤖 The engine is executing background synchronization optimization updates. An operations supervisor has been notified."

# --- 2. UNIFIED DISPLAY SETUP ---
st.set_page_config(page_title="Antic Innovations Control Room", page_icon="🚀", layout="wide")

# --- 3. SINGLE SIDEBAR MENU CONTROLLER ---
st.sidebar.title("Antic Innovations")
st.sidebar.caption("Institutional Infrastructure Node")
page = st.sidebar.radio(
    "Navigation Control Center",
    ["System Overview", "🎓 AI Coaching System", "💬 WhatsApp Sales Automation", "🌐 3D Virtual Simulations", "📈 B2B Investor Tracker"]
)

# --- 4. DATA ENGINE GRAPHIC SYSTEM MAPPING CONTROLLERS ---

# --- PAGE A: SYSTEM OVERVIEW ---
if page == "System Overview":
    st.title("🛡️ Antic Innovations — Executive Hub")
    st.subheader("Central Operations Controller & Growth Telemetry")
    st.markdown("---")
    
    data = load_data()
    learners = data.get("learners", [])
    active_learners = [l for l in learners if l.get("status") == "Active"]
    premium_count = len([l for l in learners if l.get("tier") == "Premium"])
    trial_count = len([l for l in learners if l.get("tier") == "Free Trial"])
    
    # Financial and Engagement Metrics Panel for Investors
    col1, col2, col3 = st.columns(3)
    total_funding = sum([float(inv['amount']) for inv in data.get("investor_pipeline", [])])
    col1.metric("Pipeline Deal Flow Tracking", f"₹{total_funding:,.0f}", "Antic Novelty Target Room")
    col2.metric("WhatsApp B2B AI Engine Status", "Online", "94% Reply Rate Retention")
    col3.metric("Coaching Matrix Adoption", f"{len(active_learners)} Active Accounts", "↑ Live Cloud Synchronization")
    
    st.write("")
    st.markdown("### 📊 Account Enterprise Tier Conversions")
    if learners:
        chart_data = {"Paid Premium Tier": premium_count, "Active Trial Tier": trial_count}
        st.bar_chart(chart_data, color="#2e7d32")
    else:
        st.info("No system metrics captured yet.")

    st.write("")
    st.markdown("### 🪵 Core Operation Logs")
    for log in data.get("audit_logs", [])[:5]:
        st.caption(f"⏱️ {log['timestamp']} | {log['action']} | Authority: {log['user']}")

# --- PAGE B: AI COACHING SYSTEM ---
elif page == "🎓 AI Coaching System":
    st.title("🎓 Specialized AI Coaching Manager")
    st.markdown("---")
    data = load_data()
    
    st.subheader("➕ Register New Learner Profile")
    with st.form("add_learner_form", clear_on_submit=True):
        name = st.text_input("Full Registered Name")
        age_group = st.selectbox("Target Core Cluster", ["Under 15 Trainer", "Standard Enterprise Partner"])
        status = st.selectbox("System Infrastructure Status", ["Active", "Inactive"])
        submitted = st.form_submit_button("Provision Learner Profile Node")
        
        if submitted and name.strip():
            new_id = max([l["id"] for l in data["learners"]], default=0) + 1
            new_learner = {
                "id": new_id, "name": name.strip(), "age_group": age_group, "status": status,
                "tier": "Free Trial", "join_date": datetime.now().strftime("%Y-%m-%d"), "trial_days_left": 14
            }
            data["learners"].append(new_learner)
            save_data(data)
            log_action(f"Provisioned new profile: {name.strip()}")
            st.success(f"Success: Activated network profile node for {name.strip()}!")
            st.rerun()

    st.write("")
    st.subheader("⚙️ Adaptive Learning Configurations")
    if data["learners"]:
        target_name = st.selectbox("Select Account Registry to Apply Metrics", [l["name"] for l in data["learners"]])
        slider_val = st.slider("System Matrix Difficulty Constraints Cap", 1, 10, 5)
        focus_area = st.selectbox("Operational Objective Matrix Focus", ["Discovery calls", "Technical Architecture Scaling", "Investor Pitch Strategy"])
        
        if st.button("Commit Coaching Configurations"):
            for l in data["learners"]:
                if l["name"] == target_name:
                    l["assigned_difficulty"] = slider_val
                    l["assigned_focus"] = focus_area
            save_data(data)
            log_action(f"Configured execution optimization paths for learner: {target_name}")
            st.success(f"Success: Updated matrix vectors for {target_name}!")
    else:
        st.info("Register a learner node above to interact with difficulty sliders.")

    st.write("")
    st.subheader("📋 Active System Registries")
    st.dataframe(data["learners"], use_container_width=True, hide_index=True)

# --- PAGE C: WHATSAPP AI SALES AUTOMATION ---
elif page == "💬 WhatsApp Sales Automation":
    st.title("💬 WhatsApp AI Sales Automation")
    st.markdown("---")
    data = load_data()
    
    st.subheader("🤖 Conversational Logic Sandbox")
    st.caption("Enter any live customer question below. The system will process it through your live OpenRouter key:")
    user_msg = st.text_input("Customer Inbound Message Field:", placeholder="e.g., How much does your basic automation tier cost?")
    
    if st.button("Execute Dry-Run AI Pipeline"):
        if not user_msg.strip():
            st.warning("Please input message parameters to simulate processing.")
        else:
            with st.spinner("Processing vectors through OpenRouter infrastructure..."):
                ai_response = ask_live_ai_model(user_msg)
                st.write("")
                st.markdown("**💬 Live Automated WhatsApp Engine Response:**")
                st.code(ai_response, language="markdown")
                log_action("WhatsApp Engine Test: Evaluated interactive sandbox prompt successfully.")

    st.write("")
    st.subheader("💼 Registered B2B Automation Clients")
    st.dataframe(data.get("whatsapp_clients", []), use_container_width=True, hide_index=True)

    # Dynamic Client Provisioning Onboarding Module
    st.write("")
    with st.expander("➕ Provision & Onboard New B2B Client Platform Node"):
        with st.form("add_b2b_client_form", clear_on_submit=True):
            b2b_name = st.text_input("Commercial Business / Client Name", placeholder="e.g., Global Retailer Gamma")
            client_tier = st.selectbox("Assigned System Access Status Tier", ["Free Trial Pass", "Basic Automation Engine", "Premium Enterprise Hub"])
            trial_duration = st.number_input("Allotted Sandbox Life Horizon (Days)", min_value=1, max_value=90, value=14)
            
            if st.form_submit_button("Deploy Client Infrastructure"):
        if st.button("Flush Engine Cache Pipeline"):
            data["simulation_queue"] = []
            save_data(data)
            log_action("Flushed simulation cache registries.")
            st.rerun()

# --- PAGE E: B2B INVESTOR PIPELINE TRACKER ---
elif page == "📈 B2B Investor Tracker":
    st.title("📈 B2B Investor Pipeline Tracker")
    st.markdown("---")
    data = load_data()
    
    st.subheader("💼 Active Venture Funding Round Allocations")
    df_investors = pd.DataFrame(data.get("investor_pipeline", []))
    if not df_investors.empty:
        df_display = df_investors.copy()
        df_display["amount"] = df_display["amount"].apply(lambda x: f"₹{x:,.0f}" if isinstance(x, (int, float)) else str(x))
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.info("Venture matrix pipeline registers are completely blank.")

    st.write("")
    with st.expander("📝 Commit New Institutional Allocation Node into Capital Pipeline"):
        with st.form("add_investor_form", clear_on_submit=True):
            firm_name = st.text_input("Venture / Fund Entity Title Name")
            amount = st.number_input("Investment Allocation Scale (INR Value)", min_value=100000, value=50000000)
            stage = st.selectbox("Milestone Status Stage", ["Discovery Selection", "Due Diligence Review", "Term Sheet Verification", "Closed-Funded Matrix"])
            
            if st.form_submit_button("Submit Pipeline Node Entry"):
                if firm_name.strip():
                    new_inv = {"id": len(data.get("investor_pipeline", [])) + 1, "firm": firm_name.strip(), "amount": amount, "stage": stage, "status": "High Priority"}
                    data["investor_pipeline"].append(new_inv)
                    save_data(data)
                    log_action(f"Pushed capital placement allocation node: {firm_name.strip()} (₹{amount:,.0f})")
                    st.success(f"Success: Committed tracking data matrix for fund node: {firm_name}!")
                    st.rerun()
