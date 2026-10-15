import streamlit as st
import json
import os
from datetime import datetime

# Secure Database Path Handlers
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

# --- Define Interface Pages ---
def overview_page():
    st.title("🛡️ Antic Innovations — Executive Hub")
    st.subheader("System Controller & Core Analytics")
    st.markdown("---")
    
    data = load_data()
    learners = data.get("learners", [])
    active_learners = [l for l in learners if l.get("status") == "Active"]
    premium_count = len([l for l in learners if l.get("tier") == "Premium"])
    trial_count = len([l for l in learners if l.get("tier") == "Free Trial"])
    
    # Overview metrics cards panel
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

def coaching_page():
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
            log_action(f"Registered new user profile: {name} (ID: {new_id})")
            st.success(f"Success: Profile added for {name}!")
            st.infer_button = True
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
            log_action(f"Configured operational metrics layout for: {target_name}")
            st.success("Success: Profile settings updated for the selected learner!")
    else:
        st.info("Please register a trainer or learner profile to connect configuration sliders.")

    st.subheader("📋 Active System Registries")
    st.dataframe(data["learners"])

def whatsapp_page():
    st.title("💬 WhatsApp AI Sales Automation")
    st.markdown("---")
    
    st.subheader("🤖 Conversational Logic Sandbox")
    user_msg = st.text_input("Simulate Customer Inbound Message (Type 'price' or 'trial'):").lower()
    if st.button("Run Dry-Run Test"):
        if "price" in user_msg:
            st.code("💰 Antic Innovations Automation Tier: Basic - ₹2,500/mo | Premium - ₹7,500/mo. Reply 'TRIAL' to activate a 14-day pass.")
            log_action("WhatsApp Bot: Executed automation tier billing query response.")
        elif "trial" in user_msg:
            st.code("🚀 Registration initiated. Your 14-day automated sales pilot is now syncing to port 8080.")
            log_action("WhatsApp Bot: Triggered 14-day pipeline pilot activation sequence.")
        elif user_msg:
            st.code("🤖 Antic AI Sales Bot online. How can we help automate your business conversions today?")
            log_action("WhatsApp Bot: Dispatched standard landing greeting block.")

    st.subheader("💼 Active Commercial B2B Clients")
    data = load_data()
    st.dataframe(data.get("whatsapp_clients", []))

def simulation_page():
    st.title("🌐 3D Virtual Simulations Node")
    st.markdown("---")
    
    uploaded_file = st.file_uploader("Upload Engineering Assets Node (.stl, .obj, .glb)", type=["stl", "obj", "glb"])
    if uploaded_file is not None:
        if st.button("Save Asset to Matrix Storage"):
            os.makedirs("simulation_assets", exist_ok=True)
            with open(os.path.join("simulation_assets", uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            data = load_data()
            new_id = max([s["id"] for s in data.get("simulation_queue", [])], default=0) + 1
            new_asset = {
                "id": new_id, "name": uploaded_file.name, "size_kb": round(uploaded_file.size / 1024, 2),
                "status": "Queued", "source": "User Upload"
            }
            data["simulation_queue"].append(new_asset)
            save_data(data)
            log_action(f"Uploaded engineering design block file: {uploaded_file.name}")
            st.success(f"Asset successfully uploaded and logged: {uploaded_file.name}")
            st.rerun()

    st.subheader("📦 Engineering Matrix Asset Queue")
    data = load_data()
    st.dataframe(data.get("simulation_queue", []))

def investor_page():
    st.title("📈 B2B Investor Pipeline Tracker")
    st.markdown("---")
    data = load_data()
    st.subheader("💼 Prospective Institutional Funding Rounds")
    st.dataframe(data.get("investor_pipeline", []))

# --- Application Routing Core Configuration ---
pages = [
    st.Page(overview_page, title="System Overview", icon="🛡️"),
    st.Page(coaching_page, title="AI Coaching System", icon="🎓"),
    st.Page(whatsapp_page, title="WhatsApp Sales Automation", icon="💬"),
    st.Page(simulation_page, title="3D Virtual Simulations", icon="🌐"),
    st.Page(investor_page, title="B2B Investor Tracker", icon="📈"),
]

pg = st.navigation(pages)
st.set_page_config(page_title="Antic Innovations", page_icon="🛡️", layout="wide")
pg.run()
import streamlit as st
import pandas as pd
import datetime

# --- 1. GLOBAL CONFIGURATION & SESSION STATE ---
st.set_page_config(page_title="Antic Innovations", page_icon="🚀", layout="wide")

# Initialize Mock Databases in Session State to simulate a live application backend
if "learners_db" not in st.session_state:
    st.session_state.learners_db = [
        {"name": "Arjun Sharma", "age_group": "Under 15 Trainer", "status": "Active", "tier": "Free Trial", "join_date": "2026-10-10", "trial_days_left": 7},
        {"name": "Deepa Patel", "age_group": "Under 15 Trainer", "status": "Active", "tier": "Premium", "join_date": "2026-09-15", "trial_days_left": 0},
        {"name": "Rahul Verma", "age_group": "Under 15 Trainer", "status": "Active", "tier": "Free Trial", "join_date": "2026-10-15", "trial_days_left": 14}
    ]

if "clients_db" not in st.session_state:
    st.session_state.clients_db = [
        {"id": 1, "business_name": "Local Retailer Beta", "status": "Active", "tier": "Free Trial", "join_date": "2026-10-12", "trial_days_left": 11}
    ]

if "asset_queue" not in st.session_state:
    st.session_state.asset_queue = []

if "investor_db" not in st.session_state:
    st.session_state.investor_db = [
        {"id": 1, "firm": "Antic Novelty", "amount": "$50,000,000", "stage": "Term Sheet", "status": "High Priority"}
    ]

# --- 2. NAVIGATION SIDEBAR ---
st.sidebar.title("Antic Innovations")
page = st.sidebar.radio(
    "Navigation Nodes",
    ["System Overview", "🎓 AI Coaching System", "💬 WhatsApp Sales Automation", "🌐 3D Virtual Simulations", "📈 B2B Investor Tracker"]
)

# --- PAGE 0: SYSTEM OVERVIEW ---
if page == "System Overview":
    st.title("🚀 Central Management Control Node")
    st.write("Welcome to the unified core dashboard for Antic Innovations operations.")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Learners", len(st.session_state.learners_db))
    col2.metric("B2B Automation Clients", len(st.session_state.clients_db))
    col3.metric("Queued 3D Asset Pools", len(st.session_state.asset_queue))
    col4.metric("Pipeline Deal Flow", "$50M")

# --- PAGE 1: AI COACHING SYSTEM ---
elif page == "🎓 AI Coaching System":
    st.title("🎓 Specialized AI Coaching Manager")
    
    # Section A: Register New Profile
    st.subheader("➕ Register New Learner Profile")
    with st.form("new_learner_form", clear_on_submit=True):
        learner_name = st.text_input("Learner Name", placeholder="Enter full name")
        target_cluster = st.selectbox("Target Cluster", ["Under 15 Trainer", "Advanced Matrix Specialist", "Professional Practitioner"])
        system_status = st.selectbox("System Status", ["Active", "Suspended", "On Hold"])
        
        submit_learner = st.form_submit_button("Add Learner To System")
        if submit_learner and learner_name:
            new_entry = {
                "name": learner_name,
                "age_group": target_cluster,
                "status": system_status,
                "tier": "Free Trial",
                "join_date": str(datetime.date.today()),
                "trial_days_left": 14
            }
            st.session_state.learners_db.append(new_entry)
            st.success(f"Successfully registered profile: {learner_name}")

    # Section B: Adaptive Learning Configurations
    st.subheader("⚙️ Adaptive Learning Configurations")
    learner_names = [user["name"] for user in st.session_state.learners_db]
    
    if learner_names:
        selected_learner = st.selectbox("Select Learner to Apply Profile", learner_names)
        matrix_cap = st.slider("System Matrix Difficulty Cap", min_value=1, max_value=10, value=5)
        objective_matrix = st.selectbox("Operational Objective Matrix", ["Discovery calls", "Technical onboarding", "Retention scaling"])
        
        if st.button("Save Coaching Profile"):
            st.toast(f"Profile saved! {selected_learner} capped at Matrix Level {matrix_cap} for {objective_matrix}.")
    
    # Section C: Active System Registries
    st.subheader("📋 Active System Registries")
    df_learners = pd.DataFrame(st.session_state.learners_db)
    st.dataframe(df_learners, use_container_width=True)

# --- PAGE 2: WHATSAPP AI SALES AUTOMATION ---
elif page == "💬 WhatsApp Sales Automation":
    st.title("💬 WhatsApp AI Sales Automation")
    
    # Section A: Conversational Logic Sandbox
    st.subheader("🤖 Conversational Logic Sandbox")
    st.caption("Simulate Customer Inbound Message (Type 'price' or 'trial'):")
    sim_msg = st.text_input("Simulate Customer Message Field", label_visibility="collapsed")
    
    if st.button("Run Dry-Run Test"):
        if not sim_msg:
            st.warning("Please type a sample text to trigger the conversational pipeline runtime.")
        elif "price" in sim_msg.lower():
            st.info("**AI Response Prototype Matrix:** 'Our premium pipeline options scale safely down to local frameworks. Let's schedule a deployment review strategy!'")
        elif "trial" in sim_msg.lower():
            st.info("**AI Response Prototype Matrix:** 'Your pipeline registration token is active! You can setup and configure nodes for up to 14 active sandbox loops.'")
        else:
            st.success(f"**Natural Language Router Engine:** Routed customer query '{sim_msg}' directly into adaptive classification pipelines.")

    # Section B: Active Commercial B2B Clients
    st.subheader("💼 Active Commercial B2B Clients")
    df_clients = pd.DataFrame(st.session_state.clients_db)
    st.dataframe(df_clients, use_container_width=True, hide_index=True)

# --- PAGE 3: 3D VIRTUAL SIMULATIONS ---
elif page == "🌐 3D Virtual Simulations":
    st.title("🌐 3D Virtual Simulations Node")
    
    # Section A: Upload Assets
    st.subheader("📤 Upload Engineering Assets Node (.stl, .obj, .glb)")
    uploaded_file = st.file_uploader("Upload Node", type=["stl", "obj", "glb"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize(MB)": round(uploaded_file.size / (1024*1024), 2)}
        if file_details not in st.session_state.asset_queue:
            st.session_state.asset_queue.append(file_details)
            st.success(f"Parsed asset payload queue integration: {uploaded_file.name}")

    # Section B: Asset Queue Display
    st.subheader("📦 Engineering Matrix Asset Queue")
    if len(st.session_state.asset_queue) == 0:
        st.info("Empty — Ready to parse production components or engine nodes.")
    else:
        df_assets = pd.DataFrame(st.session_state.asset_queue)
        st.dataframe(df_assets, use_container_width=True)

# --- PAGE 4: B2B INVESTOR TRACKER ---
elif page == "📈 B2B Investor Tracker":
    st.title("📈 B2B Investor Pipeline Tracker")
    
    # Section A: Prospective Funding Rounds Data view
    st.subheader("💼 Prospective Institutional Funding Rounds")
    df_investors = pd.DataFrame(st.session_state.investor_db)
    st.dataframe(df_investors, use_container_width=True, hide_index=True)
    
    # Dynamic Admin Pipeline Modifier
    with st.expander("Update Funding Milestone Criteria"):
        new_firm = st.text_input("Firm Entity Name")
        new_amt = st.text_input("Funding Allocation Range (e.g. $10,000,000)")
        new_stage = st.selectbox("Milestone Status Stage", ["Discovery", "Due Diligence", "Term Sheet", "Closed-Funded"])
        
        if st.button("Commit Node Entry to Pipeline"):
            if new_firm and new_amt:
                st.session_state.investor_db.append({
                    "id": len(st.session_state.investor_db) + 1,
                    "firm": new_firm,
                    "amount": new_amt,
                    "stage": new_stage,
                    "status": "High Priority"
                })
                st.rerun()
