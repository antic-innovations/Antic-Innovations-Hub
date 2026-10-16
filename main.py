import base64
import json
import os
import time
from typing import Any, Dict
import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="Antic Innovations Executive Hub",
    page_icon="⚡",
    layout="wide",
)

STATE_FILE = "antic_hub_state.json"
# Persistent hardcoded key as requested
OPENROUTER_API_KEY = "YOUR_ACTUAL_OPENROUTER_KEY_HERE"
GITHUB_REPO = "YOUR_USERNAME/antic-executive-hub"


def load_state() -> Dict[str, Any]:
  default = {
      "whatsapp_replies": [
          {
              "trigger": "/price",
              "response": "Hello! Retail pricing starts at ₹499.",
          }
      ],
      "marketplace_orders": [{
          "id": "ORD-101",
          "platform": "Amazon India",
          "sku": "ANT-RETRO-G3",
          "qty": 2,
          "status": "Shipped",
      }],
      "investor_pipeline": [{
          "id": 1,
          "firm": "Blume Ventures",
          "amount": 25000000,
          "stage": "Due Diligence",
          "status": "High Priority",
      }],
      "clients": [{
          "id": "Sumer11",
          "company": "Sumer Enterprise Hub",
          "status": "Active Deployment",
      }],
      "audit_logs": [
          "System Boot: Antic Executive Hub Ready with Embedded Key."
      ],
  }
  if os.path.exists(STATE_FILE):
    try:
      with open(STATE_FILE, "r", encoding="utf-8") as f:
        loaded = json.load(f)
        for k, v in default.items():
          if k not in loaded:
            loaded[k] = v
        return loaded
    except Exception:
      return default
  return default


def save_state(state: Dict[str, Any]):
  with open(STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(state, f, indent=2, ensure_ascii=False)


def log_action(state: Dict[str, Any], msg: str):
  ts = time.strftime("[%Y-%m-%d %H:%M:%S] ")
  state["audit_logs"].insert(0, ts + msg)
  if len(state["audit_logs"]) > 150:
    state["audit_logs"] = state["audit_logs"][:150]
  save_state(state)


if "hub_state" not in st.session_state:
  st.session_state.hub_state = load_state()
state = st.session_state.hub_state


def commit_file_to_github(
    file_path: str, content_str: str, commit_msg: str
) -> str:
  github_token = st.secrets.get("GITHUB_TOKEN", os.getenv("GITHUB_TOKEN", ""))
  if not github_token:
    return "⚠️ GITHUB_TOKEN missing for auto-commit."
  url = f"https://github.com{GITHUB_REPO}/contents/{file_path}"
  headers = {
      "Authorization": f"Bearer {github_token}",
      "Accept": "application/vnd.github+json",
  }
  sha = None
  r_get = requests.get(url, headers=headers, timeout=10)
  if r_get.status_code == 200:
    sha = r_get.json().get("sha")
  b64_content = base64.b64encode(content_str.encode("utf-8")).decode("utf-8")
  payload = {"message": commit_msg, "content": b64_content, "branch": "main"}
  if sha:
    payload["sha"] = sha
  r_put = requests.put(url, headers=headers, json=payload, timeout=15)
  if r_put.status_code in (200, 201):
    return f"✅ Committed {file_path}"
  return f"❌ Error {r_put.status_code}"


def run_ai(instruction: str, ctx: str) -> str:
  headers = {
      "Authorization": f"Bearer {OPENROUTER_API_KEY}",
      "Content-Type": "application/json",
  }
  payload = {
      "model": "meta-llama/llama-3.1-70b-instruct",
      "messages": [
          {"role": "user", "content": f"Context: {ctx}\nCommand: {instruction}"}
      ],
  }
  try:
    r = requests.post(
        "https://openrouter.ai",
        headers=headers,
        json=payload,
        timeout=20,
    )
    return (
        r.json()["choices"][0]["message"]["content"]
        if r.status_code == 200
        else f"API Error: {r.text}"
    )
  except Exception as e:
    return str(e)


user_email = st.secrets.get("USER_EMAIL", "owner@anticinnovations.com")
if user_email == "sumer11@clientdomain.com":
  st.title("⚡ Sumer Enterprise Workspace (mwu.streamlit.app)")
  st.success("Client: Sumer11 | Status: Active Deployment")
  if state.get("investor_pipeline"):
    df_c = pd.DataFrame(state["investor_pipeline"])[
        ["id", "firm", "amount", "stage"]
    ]
    df_c["amount"] = df_c["amount"].apply(
        lambda x: f"₹{x:,.0f}" if isinstance(x, (int, float)) else str(x)
    )
    st.dataframe(df_c, use_container_width=True, hide_index=True)
else:
  with st.sidebar:
    st.title("⚡ Antic Hub Control")
    page = st.radio(
        "Modules",
        ["🤖 AI Commander", "📊 Investors (₹)", "💬 WhatsApp", "📦 Orders", "📜 Logs"],
    )
    if st.button("🧹 Flush Cache"):
      st.cache_resource.clear()
      log_action(state, "Cache flushed.")
      st.rerun()

  if page == "🤖 AI Commander":
    st.title("🤖 Autonomous AI Commander")
    prompt = st.text_area(
        "Instruction", placeholder="Find 3 seed investors in India..."
    )
    if st.button("🚀 Execute"):
      res = run_ai(prompt, str(state))
      st.markdown(res)
      log_action(state, f"Executed AI: {prompt[:40]}")
    if st.button("💾 Commit State to GitHub"):
      st.info(
          commit_file_to_github(
              "antic_hub_state.json",
              json.dumps(state, indent=2),
              "Auto sync state",
          )
      )
  elif page == "📊 Investors (₹)":
    st.title("📊 B2B Investor Pipeline")
    df = pd.DataFrame(state.get("investor_pipeline", []))
    if not df.empty:
      df["amount"] = df["amount"].apply(lambda x: f"₹{x:,.0f}")
      st.dataframe(df, use_container_width=True, hide_index=True)
  elif page == "💬 WhatsApp":
    st.title("💬 WhatsApp Replies")
    st.dataframe(
        pd.DataFrame(state.get("whatsapp_replies", [])),
        use_container_width=True,
        hide_index=True,
    )
  elif page == "📦 Orders":
    st.title("📦 Marketplace Orders")
    st.dataframe(
        pd.DataFrame(state.get("marketplace_orders", [])),
        use_container_width=True,
        hide_index=True,
    )
  elif page == "📜 Logs":
    st.title("📜 Audit Ledger")
    for l in state.get("audit_logs", []):
      st.text(l)
