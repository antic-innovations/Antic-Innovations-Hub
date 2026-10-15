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
