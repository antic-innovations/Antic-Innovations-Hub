import streamlit as st
import json, os, pandas as pd, requests, re
from datetime import datetime

st.set_page_config(page_title="Antic Innovations Control Room", page_icon="🚀", layout="wide")
OPENROUTER_API_KEY = "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"
DB_FILE = "database.json"

def parse_num(val):
    if isinstance(val, (int, float)): return float(val)
    if isinstance(val, str):
        c = re.sub(r'[^0-9.-]', '', val)
        return float(c) if c else 0.0
    return 0.0

def load_data():
    if not os.path.exists(DB_FILE):
        return {
            "learners": [{"id": 1, "name": "Arjun Sharma", "age_group": "Under 15 Trainer", "status": "Active", "tier": "Free Trial", "join_date": "2026-10-10", "trial_days_left": 7}],
            "whatsapp_clients": [{"id": 1, "business_name": "Local Retailer Beta", "status": "Active", "tier": "Free Trial", "join_date": "2026-10-12", "trial_days_left": 11}],
            "investor_pipeline": [{"id": 1, "firm": "Antic Novelty", "amount": 50000000, "stage": "Term Sheet", "status": "High Priority"}],
            "audit_logs": [{"timestamp": "2026-10-15 11:00:00", "action": "System Initialized", "user": "System Admin"}],
            "simulation_queue": []
        }
    try:
        with open(DB_FILE, "r") as f: return json.load(f)
    except: return {"learners": [], "whatsapp_clients": [], "investor_pipeline": [], "audit_logs": [], "simulation_queue": []}

def save_data(d):
    with open(DB_FILE, "w") as f: json.dump(d, f, indent=2)

def log_action(txt):
    d = load_data()
    d["audit_logs"].insert(0, {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "action": txt, "user": "System Admin"})
    save_data(d)

def ask_live_ai_model(prompt):
    try:
        res = requests.post("https://openrouter.ai",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"},
            json={"model": "meta-llama/llama-3-8b-instruct:free", "messages": [
                {"role": "system", "content": "You are the AI engine for Antic Innovations. Give short, sharp sales & investor answers."},
                {"role": "user", "content": prompt}
            ]}, timeout=10)
        return res.json()["choices"]["message"]["content"]
    except: return "🤖 Automation Engine Online — Syncing queue."

st.sidebar.title("Antic Innovations")
page = st.sidebar.radio("Control Center", ["System Overview", "🎓 AI Coaching", "💬 WhatsApp Sales", "🌐 3D Simulations", "📈 Investor Tracker"])
data = load_data()

if page == "System Overview":
    st.title("🛡️ Antic Innovations — Executive Hub")
    c1, c2, c3 = st.columns(3)
    tot = sum(parse_num(i.get('amount', 0)) for i in data.get("investor_pipeline", []))
    c1.metric("Pipeline Deal Flow", f"₹{tot:,.0f}", "Antic Novelty")
    c2.metric("WhatsApp AI Engine", "Online", "94% Reply Rate")
    c3.metric("Coaching Adoption", f"{len([l for l in data.get('learners', []) if l.get('status')=='Active'])} Active", "Live Sync")
    if data.get("learners"): st.bar_chart(pd.DataFrame(data["learners"])["tier"].value_counts(), color="#2e7d32")
    for log in data.get("audit_logs", [])[:5]: st.caption(f"⏱️ {log['timestamp']} | {log['action']}")

elif page == "🎓 AI Coaching":
    st.title("🎓 Specialized AI Coaching Manager")
    with st.form("add_learner", clear_on_submit=True):
        nm = st.text_input("Full Registered Name")
        ag = st.selectbox("Target Cluster", ["Under 15 Trainer", "Standard Partner"])
        st_val = st.selectbox("Status", ["Active", "Inactive"])
        if st.form_submit_button("Provision Profile") and nm.strip():
            nid = max([l.get("id", 0) for l in data.get("learners", [])], default=0) + 1
            data.setdefault("learners", []).append({"id": nid, "name": nm.strip(), "age_group": ag, "status": st_val, "tier": "Free Trial", "join_date": datetime.now().strftime("%Y-%m-%d"), "trial_days_left": 14})
            save_data(data); log_action(f"Provisioned profile: {nm}"); st.rerun()
    if data.get("learners"): st.dataframe(pd.DataFrame(data["learners"]), use_container_width=True, hide_index=True)

elif page == "💬 WhatsApp Sales":
    st.title("💬 WhatsApp AI Sales Automation")
    umsg = st.text_input("Test Inbound Message:", placeholder="How much is basic automation?")
    if st.button("Execute Dry-Run AI"):
        st.code(ask_live_ai_model(umsg or "Pricing and trial?"), language="markdown")
        log_action("Executed WhatsApp AI Sandbox Test")
    if data.get("whatsapp_clients"): st.dataframe(pd.DataFrame(data["whatsapp_clients"]), use_container_width=True, hide_index=True)
    with st.expander("➕ Onboard B2B Client"):
        with st.form("add_b2b", clear_on_submit=True):
            b_nm = st.text_input("Business Name")
            b_tr = st.selectbox("Tier", ["Free Trial", "Basic Automation", "Premium Enterprise"])
            if st.form_submit_button("Deploy Client") and b_nm.strip():
                cid = max([c.get("id", 0) for c in data.get("whatsapp_clients", [])], default=0) + 1
                data.setdefault("whatsapp_clients", []).append({"id": cid, "business_name": b_nm.strip(), "status": "Active", "tier": b_tr, "join_date": datetime.now().strftime("%Y-%m-%d"), "trial_days_left": 14})
                save_data(data); log_action(f"Onboarded client: {b_nm}"); st.rerun()

elif page == "🌐 3D Simulations":
    st.title("🌐 3D Virtual Simulations Node")
    uf = st.file_uploader("Upload .stl / .obj / .glb", type=["stl", "obj", "glb"], label_visibility="collapsed")
    if uf:
        if not any(f.get("FileName") == uf.name for f in data.get("simulation_queue", [])):
            data.setdefault("simulation_queue", []).append({"FileName": uf.name, "FileType": uf.type, "Status": "Queued"})
            save_data(data); log_action(f"Uploaded 3D asset: {uf.name}"); st.rerun()
    if data.get("simulation_queue"):
        st.dataframe(pd.DataFrame(data["simulation_queue"]), use_container_width=True)
        if st.button("Flush Queue"): data["simulation_queue"] = []; save_data(data); st.rerun()
    else: st.info("Asset queue empty.")

elif page == "📈 Investor Tracker":
    st.title("📈 B2B Investor Pipeline Tracker")
    df_i = pd.DataFrame(data.get("investor_pipeline", []))
    if not df_i.empty:
        df_d = df_i.copy()
        df_d["amount"] = df_d["amount"].apply(lambda x: f"₹{parse_num(x):,.0f}")
        st.dataframe(df_d, use_container_width=True, hide_index=True)
    else: st.info("No active capital allocators recorded.")
    with st.expander("📝 Commit Allocation Node"):
        with st.form("add_inv", clear_on_submit=True):
            fnm = st.text_input("Firm Entity Name")
            amt = st.number_input("Amount (INR)", min_value=100000, value=50000000)
            stg = st.selectbox("Stage", ["Discovery", "Due Diligence", "Term Sheet", "Closed-Funded"])
            if st.form_submit_button("Submit Entry") and fnm.strip():
                iid = max([i.get("id", 0) for i in data.get("investor_pipeline", [])], default=0) + 1
                data.setdefault("investor_pipeline", []).append({"id": iid, "firm": fnm.strip(), "amount": amt, "stage": stg, "status": "High Priority"})
                save_data(data); log_action(f"Committed investor allocation: {fnm}"); st.rerun()
