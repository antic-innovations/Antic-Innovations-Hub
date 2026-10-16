import json
import os
import requests
import streamlit as st

# ==========================================
# 1. PASTE YOUR KEY HERE (Line 11 - Quick Local Fallback)
# ==========================================
FALLBACK_API_KEY = ""  # Example: " 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 "


# Option B: Streamlit Cloud Secrets (App Settings -> Secrets)
# Option C: Left Sidebar input field at runtime
def get_active_api_key():
  if "openrouter_key" in st.session_state and st.session_state.openrouter_key:
    return st.session_state.openrouter_key.strip()
  try:
    if "OPENROUTER_API_KEY" in st.secrets and st.secrets["OPENROUTER_API_KEY"]:
      return str(st.secrets["OPENROUTER_API_KEY"]).strip()
  except Exception:
    pass
  return FALLBACK_API_KEY.strip()


# ==========================================
# 2. INITIALIZE SESSION STATE & SAFE DEFAULTS
# ==========================================
STATUS_OPTIONS = ["Idle", "Ready", "Running", "Completed"]

if "projects" not in st.session_state:
  st.session_state.projects = [
      {
          "id": "proj_01",
          "name": "Core Innovation Engine",
          "status": "Running",
          "code": (
              "def run_engine():\n    return 'Engine active with OpenRouter"
              " telemetry.'"
          ),
      },
      {
          "id": "proj_02",
          "name": "Google Sites & Docs Sync",
          "status": "Running",
          "code": (
              "def sync_site():\n    return 'Synced with"
              " sites.google.com/view/antic-innovations'"
          ),
      },
      {
          "id": "proj_03",
          "name": "Automated Code Synthesizer",
          "status": "Running",
          "code": "def generate_module():\n    return 'Ready to synthesize.'",
      },
  ]

# ==========================================
# 3. SIDEBAR CONTROLS (Runtime Key Input)
# ==========================================
with st.sidebar:
  st.title("⚡ Antic Control Hub")

  # You can type/paste your key directly in this box when the app loads:
  user_key_input = st.text_input(
      "OpenRouter API Key",
      value=st.session_state.get("openrouter_key", ""),
      type="password",
      help="Paste your sk-or-... key here",
  )
  if user_key_input:
    st.session_state.openrouter_key = user_key_input

  selected_model = st.selectbox(
      "Router Model",
      [
          "openrouter/auto",
          "deepseek/deepseek-r1",
          "anthropic/claude-3.5-sonnet",
      ],
  )
  st.text_input(
      "Google Sites Reference URL",
      value="https://sites.google.com/view/antic-innovations",
      disabled=True,
  )


# ==========================================
# 4. API CALL HELPER WITH FIXED HEADERS
# ==========================================
def call_openrouter(prompt, model=None):
  active_key = get_active_api_key()
  if not active_key or len(active_key) < 10:
    return "❌ Error: Missing or invalid OpenRouter API Key. Enter it in Line 11, the sidebar, or Streamlit Secrets."

  headers = {
      "Authorization": f"Bearer {active_key}",
      "HTTP-Referer": "https://antic-innovations.streamlit.app",
      "X-Title": "Antic Innovations Hub",
      "Content-Type": "application/json",
  }
  payload = {
      "model": model or selected_model,
      "messages": [{"role": "user", "content": prompt}],
  }
  try:
    res = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30,
    )
    if res.status_code == 200:
      return res.json()["choices"]["message"]["content"]
    else:
      return f"⚠️ API Error ({res.status_code}): {res.text}"
  except Exception as e:
    return f"🚨 Request Exception: {str(e)}"


# ==========================================
# 5. SAFE STATUS SELECTBOX (FIXES VALUEERROR)
# ==========================================
st.title("Antic Innovations — Autonomous App & Project Manager")

for proj in st.session_state.projects:
  with st.expander(
      f"[{str(proj.get('status','Idle')).upper()}] {proj['name']} (ID:"
      f" {proj['id']})"
  ):
    curr_stat = proj.get("status", "Idle")
    # Case-insensitive safe index resolution prevents ValueError
    try:
      safe_idx = next(
          i
          for i, opt in enumerate(STATUS_OPTIONS)
          if opt.lower() == str(curr_stat).lower()
      )
    except StopIteration:
      safe_idx = 0

    new_stat = st.selectbox(
        "Status",
        STATUS_OPTIONS,
        index=safe_idx,
        key=f"stat_{proj['id']}",
    )
    proj["status"] = new_stat

    if st.button(f"Optimize via AI ({proj['id']})", key=f"opt_{proj['id']}"):
      res = call_openrouter(
          "Audit and optimize this Python code for"
          f" {proj['name']}:\n{proj['code']}"
      )
      st.code(res, language="markdown")
