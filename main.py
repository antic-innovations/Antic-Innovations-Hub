import os
import json
import streamlit as st
import requests

st.set_page_config(
    page_title="Antic Innovations | AI Project Manager",
    page_icon="⚡",
    layout="wide"
)

if "projects" not in st.session_state:
    st.session_state.projects = [
        {
            "id": "proj-01",
            "name": "Core Innovation Engine",
            "status": "Active",
            "category": "Architecture",
            "description": "Base multi-agent router and execution supervisor.",
            "code_snippet": "def run_engine():\n    return 'Engine active with OpenRouter telemetry.'",
            "logs": ["Initialized core loop."]
        },
        {
            "id": "proj-02",
            "name": "Google Sites & Docs Sync",
            "status": "Ready",
            "category": "Integration",
            "description": "Synchronizes portfolio structure and documentation artifacts.",
            "code_snippet": "def sync_site(url):\n    return f'Synced metadata from {url}'",
            "logs": ["Linked portfolio index."]
        },
        {
            "id": "proj-03",
            "name": "Automated Code Synthesizer",
            "status": "Idle",
            "category": "Generator",
            "description": "Generates modular Streamlit/Python micro-tools on demand.",
            "code_snippet": "def synthesize(prompt):\n    return '# Generated module\npass'",
            "logs": ["Ready for prompts."]
        }
    ]

if "ai_chat_history" not in st.session_state:
    st.session_state.ai_chat_history = []

with st.sidebar:
    st.title("⚡ Antic Control Hub")
    api_key_input = st.text_input(
        "OpenRouter API Key",
        value=os.environ.get("OPENROUTER_API_KEY", ""),
        type="password",
        help="Enter your openrouter.ai key (sk-or-...)"
    )
    selected_model = st.selectbox(
        "Router Model",
        ["openrouter/auto", "deepseek/deepseek-r1", "anthropic/claude-3.5-sonnet", "google/gemini-2.5-flash"],
        index=0
    )
    site_reference = st.text_input("Google Sites Reference URL", value="https://sites.google.com/view/antic-innovations")
    
    st.divider()
    st.subheader("Master Actions")
    if st.button("🔄 Execute All Projects"):
        for p in st.session_state.projects:
            p["status"] = "Running"
            p["logs"].append("Executed batch cycle via master orchestrator.")
        st.rerun()

    if st.button("➕ New Project Module"):
        new_id = f"proj-{len(st.session_state.projects)+1:02d}"
        st.session_state.projects.append({
            "id": new_id,
            "name": f"Module {new_id.upper()}",
            "status": "Idle",
            "category": "Custom",
            "description": "Newly created project slot.",
            "code_snippet": "# Write logic here\ndef execute():\n    pass",
            "logs": ["Created project slot."]
        })
        st.rerun()

def call_openrouter(prompt, system_instruction="You are the AI Master Controller for Antic Innovations."):
    if not api_key_input:
        return "⚠️ Please enter your OpenRouter API Key in the sidebar to activate AI management."
    
    headers = {
        "Authorization": f"Bearer {api_key_input}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/antic-innovations/streamlit-app",
        "X-Title": "Antic Innovations AI Manager"
    }
    payload = {
        "model": selected_model,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }
    try:
        resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        else:
            return f"API Error ({resp.status_code}): {resp.text}"
    except Exception as e:
        return f"Request failed: {str(e)}"

st.title("Antic Innovations — Autonomous App & Project Manager")
st.caption(f"Portfolio Sync Source: {site_reference} | Active Engine: {selected_model}")

tab_dash, tab_ai, tab_code, tab_github = st.tabs(["📊 Project Dashboard", "🤖 AI Master Controller", "💻 Live Code Editor", "🐙 GitHub Deployment"])

with tab_dash:
    col1, col2, col3, col4 = st.columns(4)
    total_p = len(st.session_state.projects)
    active_p = sum(1 for p in st.session_state.projects if p["status"] == "Running")
    ready_p = sum(1 for p in st.session_state.projects if p["status"] == "Ready")
    idle_p = sum(1 for p in st.session_state.projects if p["status"] == "Idle")
    
    col1.metric("Total Projects", total_p)
    col2.metric("Running", active_p)
    col3.metric("Ready", ready_p)
    col4.metric("Idle", idle_p)
    
    st.divider()
    for idx, proj in enumerate(st.session_state.projects):
        with st.expander(f"[{proj['status'].upper()}] {proj['name']} ({proj['category']})", expanded=(idx==0)):
            c_info, c_ctrl = st.columns([3, 1])
            with c_info:
                st.write(f"**ID:** `{proj['id']}`")
                st.write(f"**Description:** {proj['description']}")
                st.text_area("Recent Execution Logs", value="\n".join(proj['logs'][-5:]), height=80, key=f"log_{proj['id']}", disabled=True)
            with c_ctrl:
                new_stat = st.selectbox("Status", ["Idle", "Ready", "Running", "Completed"], index=["Idle", "Ready", "Running", "Completed"].index(proj['status']), key=f"stat_{proj['id']}")
                if new_stat != proj['status']:
                    proj['status'] = new_stat
                    proj['logs'].append(f"Status changed to {new_stat}")
                    st.rerun()
                if st.button("Run Project Logic", key=f"run_btn_{proj['id']}"):
                    proj['status'] = "Running"
                    proj['logs'].append("Executed manual trigger.")
                    st.rerun()
                if st.button("Optimize via AI", key=f"ai_opt_{proj['id']}"):
                    prompt_txt = f"Optimize and refactor this Python snippet for project '{proj['name']}':\n```python\n{proj['code_snippet']}\n```"
                    res = call_openrouter(prompt_txt)
                    proj['logs'].append("AI Optimization completed.")
                    st.session_state[f"ai_res_{proj['id']}"] = res
                    st.rerun()
            
            if f"ai_res_{proj['id']}" in st.session_state:
                st.markdown("**AI Optimization Output:**")
                st.code(st.session_state[f"ai_res_{proj['id']}"], language="markdown")

with tab_ai:
    st.subheader("Global AI Master Controller")
    st.write("Instruct the AI to orchestrate all projects, debug errors, or generate architecture plans.")
    
    for msg in st.session_state.ai_chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    user_prompt = st.chat_input("Ask the AI to manage, audit, or write code across all Antic projects...")
    if user_prompt:
        st.session_state.ai_chat_history.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)
            
        context_payload = f"Current Projects State:\n{json.dumps(st.session_state.projects, indent=2)}\n\nUser Command:\n{user_prompt}"
        ai_reply = call_openrouter(context_payload, system_instruction="You are the Lead Systems Architect of Antic Innovations. You manage multiple Python/Streamlit project modules, write clean code, and output actionable execution plans.")
        
        st.session_state.ai_chat_history.append({"role": "assistant", "content": ai_reply})
        with st.chat_message("assistant"):
            st.markdown(ai_reply)

with tab_code:
    st.subheader("Multi-Project Code Studio")
    selected_proj_name = st.selectbox("Select Project to Edit", [p["name"] for p in st.session_state.projects], key="sel_proj_code")
    target_proj = next(p for p in st.session_state.projects if p["name"] == selected_proj_name)
    
    updated_code = st.text_area(
        "Python Implementation",
        value=target_proj["code_snippet"],
        height=300,
        key=f"editor_{target_proj['id']}"
    )
    if st.button("Save & Commit Code", key="save_commit_code"):
        target_proj["code_snippet"] = updated_code
        target_proj["logs"].append("Updated code snippet in studio.")
        st.success(f"Saved code for {target_proj['name']}")

with tab_github:
    st.subheader("GitHub Repository Structure & Export")
    st.write("Push these files to your GitHub repository (`antic-innovations-app`) and deploy to Streamlit Cloud.")
    
    st.markdown("### `requirements.txt`")
    req_txt = "streamlit>=1.38.0\nrequests>=2.31.0\npydantic>=2.0.0"
    st.code(req_txt, language="text")
    
    st.markdown("### `README.md`")
    readme_txt = "# Antic Innovations AI Manager\n\nAutonomous Streamlit portfolio and multi-project orchestrator powered by OpenRouter.\n\n## Setup\n1. Clone repo\n2. `pip install -r requirements.txt`\n3. Set `OPENROUTER_API_KEY` or input in sidebar\n4. Run `streamlit run app.py`\n"
    st.code(readme_txt, language="markdown")
    
    st.markdown("### Deploy to Streamlit Community Cloud")
    st.info("1. Push `app.py` and `requirements.txt` to GitHub.\n2. Connect repo on share.streamlit.io.\n3. Add `OPENROUTER_API_KEY` under App Settings -> Secrets.")
