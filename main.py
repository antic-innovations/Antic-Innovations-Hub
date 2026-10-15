import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# --- 1. SECURE DATABASE PATH HANDLERS ---
DB_FILE = "database.json"

def load_data():
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
                {"timestamp": "2026-10-15 11:00:00", "action": "System Initialized", "user": "System Admin"}
            ], 
            "simulation_queue": []
        }
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

# --- 2. SINGLE SIDEBAR MENU CONTROLLER ---
st.sidebar.title("Antic Innovations")
page = st.sidebar.radio(
    "Navigation Nodes",
    ["System Overview", "🎓 AI Coaching System", "💬 WhatsApp Sales Automation", "🌐 3D Virtual Simulations", "📈 B2B Investor Tracker"]
)

# --- 3. PAGE LOGER BRANCHES ---

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
            log_action(f"Registered new user profile: {name} (ID: {new_id})")
            st.success(f"Success: Profile added for {name}!")
            st.hybrid_rerun = True
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
    user_msg = st.text_input("Simulate Customer Inbound Message (Type 'price' or 'trial'):")
    
    if st.button("Run Dry-Run Test"):
        if not user_msg.strip():
            st.warning("Please enter a custom test query parameter pattern.")
        elif "price" in user_msg.lower() or "cost" in user_msg.lower():
            st.code("💰 Antic Innovations Automation Tier: Basic - ₹2,500/mo | Premium - ₹7,500/mo. Reply 'TRIAL' to activate a 14-day pass.")
            log_action("WhatsApp Bot Run: Executed automated billing message routing.")
        elif "trial" in user_msg.lower() or "free" in user_msg.lower():
            st.code("🚀 Registration token status active! Welcome to the Antic Sandboxed Environment node.")
            log_action("WhatsApp Bot Run: Activated demo token simulation pipeline.")
        else:
            st.success(f"Routed standard question parameter down general query classification lines.")

    st.subheader("💼 Active Commercial B2B Clients")
    st.dataframe(data.get("whatsapp_clients", []), use_container_width=True, hide_index=True)

# --- VIEW D: 3D VIRTUAL SIMULATIONS NODE ---
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
            log_action(f"Uploaded 3D structural matrix mesh node file: {uploaded_file.name}")
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
            log_action("Flushed active mechanical visualization components catalog cache.")
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
            firm = st.text_input("Firm Entity Name")
            amount = st.number_value = st.number_input("Funding Allocation Range (INR)", min_value=100000, value=50000000)
            stage = st.selectbox("Milestone Status Stage", ["Discovery", "Due Diligence", "Term Sheet", "Closed-Funded"])
            
            if st.form_submit_button("Submit Pipeline Entry"):
                if firm.strip():
                    new_inv = {"id": len(data.get("investor_pipeline", [])) + 1, "firm": firm.strip(), "amount": amount, "stage": stage, "status": "High Priority"}
                    data["investor_pipeline"].append(new_inv)
                    save_data(data)
import requests

def send_live_whatsapp_message(customer_phone, reply_text):
    """
    Triggers an official live WhatsApp message transmission 
    directly to a customer's device using Meta Graph API infrastructure nodes.
    """
    # Replace these placeholders with your actual Meta Developer credentials
    ACCESS_TOKEN = "YOUR_META_PERMANENT_ACCESS_TOKEN"
    PHONE_NUMBER_ID = "YOUR_META_WHATSAPP_PHONE_NUMBER_ID"
    
    url = f"https://facebook.com{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": customer_phone,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": reply_text
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}
from fastapi import FastAPI, Request, Response
import uvicorn
from threading import Thread

# Create a background FastAPI engine specifically for the Webhook listener
api = FastAPI()

VERIFY_TOKEN = "AnticAutomationToken2026"  # Put this exact phrase inside your Meta Dashboard

@api.get("/webhook")
def meta_verification(request: Request):
    """
    Step 1: The Handshake. Meta pings this URL once when you save it 
    in their developer portal to verify your app is real.
    """
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return Response(content=challenge, media_type="text/plain")
    return Response(content="Verification Failed", status_code=403)


@api.post("/webhook")
async def receive_whatsapp_message(request: Request):
    """
    Step 2: The Ear. Meta hits this block every single time a customer 
    sends a real WhatsApp message to your client's number.
    """
    payload = await request.json()
    
    try:
        # Extract the incoming text message and the sender's phone number from Meta's deep JSON data layout
        entry = payload["entry"][0]["changes"][0]["value"]
        if "messages" in entry:
            customer_phone = entry["messages"][0]["from"]
            message_body = entry["messages"][0]["text"]["body"].lower()
            
            # --- Your AI Automation Logic ---
            if "price" in message_body or "cost" in message_body:
                reply = "💰 Antic Innovations Automation Tier: Basic - ₹2,500/mo | Premium - ₹7,500/mo."
            elif "trial" in message_body:
                reply = "🚀 Registration token active! Welcome to Antic Innovations."
            else:
                reply = "👋 Thank you for messaging us! An advisor will review your query shortly."
                
            # Automatically send the live WhatsApp text back to the customer's phone!
            # send_live_whatsapp_message(customer_phone, reply)
            
    except Exception as e:
        pass # Prevents minor parsing issues from freezing your background API thread
        
    return {"status": "success"}

# Function to run this server concurrently in the background of your Streamlit app
def run_webhook_listener():
    uvicorn.run(api, host="0.0.0.0", port=8000)

# Starts the background engine seamlessly without disturbing your main display layout
Thread(target=run_webhook_listener, daemon=True).start()
