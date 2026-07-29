from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version
from chat import now_iso, run_model_tool_loop, safe_slug, trim_history

ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
TRANSCRIPTS_DIR = ROOT / "transcripts"
load_lab_env(ROOT)

st.set_page_config(page_title="Research Agent — G31", page_icon="🔎", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []
if "turns" not in st.session_state:
    st.session_state.turns = []
if "transcript_id" not in st.session_state:
    st.session_state.transcript_id = None

st.title("🔎 Research Agent — G31")
st.caption(
    "Nhập request, xem agent chọn tool nào, args gì, kết quả/lỗi ra sao, "
    "và biết đang chạy version/artifact nào. Mỗi phiên tự lưu transcript JSON."
)

with st.sidebar:
    st.header("Cấu hình")
    provider_name = st.selectbox("Provider", ["openai", "openrouter", "anthropic", "gemini"], index=0)
    version = st.text_input("Version", value="v3")
    max_tool_rounds = st.number_input("Max tool rounds", min_value=1, max_value=10, value=4)
    history_window = st.number_input("History window (turns giữ lại)", min_value=0, max_value=20, value=5)

    if st.button("🔄 Reset hội thoại", use_container_width=True):
        st.session_state.history = []
        st.session_state.turns = []
        st.session_state.transcript_id = None
        st.rerun()

    st.divider()

    system_prompt_path = ARTIFACTS_DIR / "system_prompt.md"
    tools_path = ARTIFACTS_DIR / "tools.yaml"
    artifact_version = build_artifact_version(version, system_prompt_path, tools_path)

    st.markdown("**Artifact version**")
    st.code(artifact_version.artifact_version, language="text")
    st.caption(f"prompt_hash: {artifact_version.prompt_hash[:12]}")
    st.caption(f"tools_hash: {artifact_version.tools_hash[:12]}")
    if st.session_state.transcript_id:
        st.caption(f"transcript: {st.session_state.transcript_id}.transcript.json")


def render_round(round_record: dict[str, Any]) -> None:
    calls = round_record.get("tool_calls", [])
    results = round_record.get("tool_results", [])
    label = f"Round {round_record['round']} — {len(calls)} tool call(s)" if calls else f"Round {round_record['round']} — no tool call"
    with st.expander(label, expanded=True):
        if round_record.get("assistant_text"):
            st.markdown(f"_Model note:_ {round_record['assistant_text']}")
        for call, event in zip(calls, results):
            st.markdown(f"**Tool:** `{call['name']}`")
            st.json(call["args"], expanded=False)
            result = event.get("result", {})
            if isinstance(result, dict) and result.get("error"):
                st.error(f"error: {result.get('error')} — {result.get('message', '')}")
            else:
                st.json(result, expanded=False)


def save_transcript() -> None:
    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    if st.session_state.transcript_id is None:
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
        st.session_state.transcript_id = "_".join(["ui", safe_slug(version), safe_slug(provider_name), timestamp])
    transcript_path = TRANSCRIPTS_DIR / f"{st.session_state.transcript_id}.transcript.json"
    transcript = {
        "transcript_id": st.session_state.transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider_name,
        "system_prompt": str(system_prompt_path),
        "tools": str(tools_path),
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
        "updated_at": now_iso(),
        "turns": st.session_state.turns,
    }
    transcript_path.write_text(json.dumps(transcript, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


# --- render existing conversation ---
for turn in st.session_state.turns:
    with st.chat_message("user"):
        st.write(turn["user"])
    with st.chat_message("assistant"):
        if turn["status"] == "waiting_for_user":
            st.info(f"❓ {turn['assistant_text']}")
        elif turn["status"] == "provider_error":
            st.error(turn["assistant_text"])
        else:
            st.write(turn["assistant_text"])
        for round_record in turn["rounds"]:
            render_round(round_record)
        st.caption(f"status: {turn['status']} · artifact_version: {turn['artifact_version']}")

# --- handle new input ---
user_text = st.chat_input("Nhập yêu cầu (vd: 'Tìm tin AI hôm nay và tóm tắt 3 kết quả')...")

if user_text:
    with st.chat_message("user"):
        st.write(user_text)

    system_prompt = system_prompt_path.read_text(encoding="utf-8")
    tool_declarations = load_tool_declarations(tools_path)
    openai_tools = to_openai_tools(tool_declarations)

    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.history, history_window),
        {"role": "user", "content": user_text},
    ]

    with st.chat_message("assistant"):
        with st.spinner("Agent đang chọn tool và chạy..."):
            try:
                provider = make_provider(provider_name)
                result = run_model_tool_loop(
                    provider=provider,
                    messages=messages,
                    tools=openai_tools,
                    model=None,
                    max_tool_rounds=int(max_tool_rounds),
                )
            except Exception as exc:
                result = {
                    "status": "provider_error",
                    "assistant_text": f"{type(exc).__name__}: {exc}",
                    "rounds": [],
                    "tool_events": [],
                }

        status = result["status"]
        assistant_text = result["assistant_text"]
        if status == "waiting_for_user":
            st.info(f"❓ {assistant_text}")
        elif status == "provider_error":
            st.error(assistant_text)
        else:
            st.write(assistant_text)
        for round_record in result["rounds"]:
            render_round(round_record)
        st.caption(f"status: {status} · artifact_version: {artifact_version.artifact_version}")

    st.session_state.history.append({"role": "user", "content": user_text})
    st.session_state.history.append({"role": "assistant", "content": assistant_text})
    st.session_state.turns.append({
        "turn_index": len(st.session_state.turns) + 1,
        "started_at": now_iso(),
        "user": user_text,
        "status": status,
        "assistant_text": assistant_text,
        "rounds": result["rounds"],
        "tool_events": result["tool_events"],
        "artifact_version": artifact_version.artifact_version,
        "ended_at": now_iso(),
    })
    save_transcript()
