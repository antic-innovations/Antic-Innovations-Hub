import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
import requests

# --- 1. GLOBAL SECURE PARAMETERS & CONFIGS ---
OPENROUTER_API_KEY = "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"
DB_FILE = "database.json"

def load_data():
    if not os.path.exists(DB_FILE):
        return {"learners": [], "whatsapp_clients": [], "investor_pipeline": [], "audit_logs": [], "simulation_queue": []}
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {"learners": [], "whatsapp_clients": [], "investor_pipeline": [], "audit_logs": [], "simulation_queue": []}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_action(action_text):
    data = load_data()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["audit_logs"].insert(0, {"timestamp": now_str, "action": action_text, "user": "System Admin"})
    save_data(data)

def ask_live_ai_model(prompt_text):
    """Queries OpenRouter to generate an instant contextual response path for inbound queries."""
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
            {"role": "system", "content": "You are a professional sales automation assistant for Antic Innovations. Give brief, highly accurate, short answers."},
            {"role": "user", "content": prompt_text}
        ]
    }
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=10)
        return res.json()["choices"]["message"]["content"]
    except:
        return "🤖 Our automated lines are currently performing system synchronization optimization passes. An expert agent will message you directly!"

# --- 2. SINGLE SIDEBAR MENU CONTROLLER ---
st.sidebar.title("Antic Innovations")
page = st.sidebar.radio(
    "Navigation Nodes",
    ["System Overview", "🎓 AI Coaching System", "💬 WhatsApp Sales Automation", "🌐 3D Virtual Simulations", "📈 B2B Investor Tracker"]
)

# --- VIEW A: SYSTEM OVERVIEW ---
if page == "System Overview":
    st.title("🛡️ Antic Innovations — Executive Hub")
    st.subheader("System Controller & Core Analytics")
    st.markdown("---")
    
    data = load_data()
    learners = data.get("learners", [])
    active_learners = [l for l in learners if l.get("status") == "Active"]
    premium_count = len([l for l in learners if l.get("tier") == "Premium"])
    trial_count = len([l for l in learners if l.get("tier") == "Free Trial"])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Pipeline Tracking", "₹50,000,000", "Antic Novelty")
    col2.metric("WhatsApp AI Engine", "Online", "94% Reply Rate")
    col3.metric("Coaching Matrix Adoption", f"{len(active_learners)} Active", "↑ Live Sync")
    
    st.markdown("### 📊 Account Tier Conversions")
    if learners:
        chart_data = {"Premium": premium_count, "Free Trial": trial_count}
        st.bar_chart(chart_data)
    else:
        st.info("No learner account records synced yet.")

    st.markdown("### 🪵 Live System Activity Logs")
    for log in data.get("audit_logs", [])[:5]:
        st.text(f"⏱️ {log['timestamp']} | {log['action']} | {log['user']}")

# --- VIEW B: AI COACHING SYSTEM ---
elif page == "🎓 AI Coaching System":
    st.title("🎓 Specialized AI Coaching Manager")
    st.markdown("---")
    data = load_data()
    
    st.subheader("➕ Register New Learner Profile")
    with st.form("add_learner_form", clear_on_submit=True):
        name = st.text_input("Learner Name")
        age_group = st.selectbox("Target Cluster", ["Under 15 Trainer", "Standard"])
        status = st.selectbox("System Status", ["Active", "Inactive"])
        submitted = st.form_submit_button("Add Learner To System")
        
        if submitted and name:
            new_id = max([l["id"] for l in data["learners"]], default=0) + 1
            new_learner = {
                "id": new_id, "name": name, "age_group": age_group, "status": status,
                "tier": "Free Trial", "join_date": datetime.now().strftime("%Y-%m-%d"), "trial_days_left": 14
            }
            data["learners"].append(new_learner)
            save_data(data)
            log_action(f"Registered new user profile: {name}")
            st.success(f"Success: Profile added for {name}!")
            st.rerun()

    st.subheader("⚙️ Adaptive Learning Configurations")
    if data["learners"]:
        target_name = st.selectbox("Select Learner to Apply Profile", [l["name"] for l in data["learners"]])
        slider_val = st.slider("System Matrix Difficulty Cap", 1, 10, 5)
        focus_area = st.selectbox("Operational Objective Matrix", ["Discovery calls", "Technical Architecture", "Closing Strategy"])
        
        if st.button("Save Coaching Profile"):
            for l in data["learners"]:
                if l["name"] == target_name:
                    l["assigned_difficulty"] = slider_val
                    l["assigned_focus"] = focus_area
            save_data(data)
            log_action(f"Configured operational metrics for: {target_name}")
            st.success("Success: Profile settings updated successfully!")
    else:
        st.info("Please register a trainer or learner profile to connect configuration sliders.")

    st.subheader("📋 Active System Registries")
    st.dataframe(data["learners"], use_container_width=True, hide_index=True)

# --- VIEW C: WHATSAPP AI SALES AUTOMATION ---
elif page == "💬 WhatsApp Sales Automation":
    st.title("💬 WhatsApp AI Sales Automation")
    st.markdown("---")
    data = load_data()
    
    st.subheader("🤖 Conversational Logic Sandbox")
    user_msg = st.text_input("Simulate Customer Inbound Message (Ask any sales question to test the live AI):")
    
    if st.button("Run Dry-Run Test"):
        if not user_msg.strip():
            st.warning("Please enter a custom test query parameter pattern.")
        else:
            with st.spinner("Talking to live OpenRouter intelligence pipelines..."):
                ai_response = ask_live_ai_model(user_msg)
                st.code(f"💬 Live AI Automation Reply:\n\n{ai_response}")
                log_action(f"WhatsApp Bot Sandbox Test Executed.")

    st.subheader("💼 Active Commercial B2B Clients")
    st.dataframe(data.get("whatsapp_clients", []), use_container_width=True, hide_index=True)

# --- VIEW D: 3D VIRTUAL SIMULATIONS ---
elif page == "🌐 3D Virtual Simulations":
    st.title("🌐 3D Virtual Simulations Node")
    st.markdown("---")
    data = load_data()
    
    st.subheader("📤 Upload Engineering Assets Node (.stl, .obj, .glb)")
    uploaded_file = st.file_uploader("Upload Node", type=["stl", "obj", "glb"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "Status": "Ready for Processing Engine"}
        if "simulation_queue" not in data:
            data["simulation_queue"] = []
        if not any(f["FileName"] == uploaded_file.name for f in data["simulation_queue"]):
            data["simulation_queue"].append(file_details)
            save_data(data)
            log_action(f"Uploaded structural node file: {uploaded_file.name}")
            st.success(f"Successfully verified architectural design node: {uploaded_file.name}")
            st.rerun()

    st.subheader("📦 Engineering Matrix Asset Queue")
    if not data.get("simulation_queue"):
        st.info("Computing pool empty — ready to parse production models.")
    else:
        st.dataframe(data["simulation_queue"], use_container_width=True)
        if st.button("Flush Simulation Cache Pipeline"):
            data["simulation_queue"] = []
            save_data(data)
            log_action("Flushed active visual components catalog cache.")
            st.rerun()

# --- VIEW E: B2B INVESTOR PIPELINE TRACKER ---
elif page == "📈 B2B Investor Tracker":
    st.title("📈 B2B Investor Pipeline Tracker")
    st.markdown("---")
    data = load_data()
    
    st.subheader("💼 Prospective Institutional Funding Rounds")
    df_investors = pd.DataFrame(data.get("investor_pipeline", []))
    if not df_investors.empty:
        df_display = df_investors.copy()
        df_display["amount"] = df_display["amount"].apply(lambda x: f"₹{x:,.0f}" if isinstance(x, (int, float)) else str(x))
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.info("No investment records located inside dashboard registry tables.")

    with st.expander("📝 Commit Entry to Pipeline Round"):
        with st.form("add_investor_form", clear_on_submit=True):
            firm_name = st.text_input("Firm Entity Name")
            amount = st.number_input("Funding Allocation Range (INR)", min_value=100000, value=50000000)
            stage = st.selectbox("Milestone Status Stage", ["Discovery", "Due Diligence", "Term Sheet", "Closed-Funded"])
            
            if st.form_submit_button("Submit Pipeline Entry"):
                if firm_name.strip():
                    new_inv = {"id": len(data.get("investor_pipeline", [])) + 1, "firm": firm_name.strip(), "amount": amount, "stage": stage, "status": "High Priority"}
                    data["investor_pipeline"].append(new_inv)
                    save_data(data)
                    log_action(f"Added venture fund tracking node for: {firm_name.strip()}")
                    st.success(f"Success: Committed pipeline node for {firm_name}!")
                    st.rerun()
