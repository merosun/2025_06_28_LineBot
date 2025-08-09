import os
import streamlit as st
from google import genai

# 基本設定
st.set_page_config(page_title="Gemini Chat", page_icon="💬")
API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"

if not API_KEY:
    st.error("請先設定 GEMINI_API_KEY 環境變數")
    st.stop()

client = genai.Client(api_key=API_KEY)

# 對話歷史存在 session
if "history" not in st.session_state:
    st.session_state.history = []  # 元素: {"role":"user"/"assistant", "text":"..."}

st.title("💬 Gemini Chat（繁體中文）")

# 顯示歷史
for m in st.session_state.history:
    with st.chat_message("user" if m["role"] == "user" else "assistant"):
        st.markdown(m["text"])

# 輸入框
user_input = st.chat_input("輸入你的問題…")
if user_input:
    st.session_state.history.append({"role": "user", "text": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 把歷史組成一段文字（簡單保存上下文）
    def build_prompt(history):
        lines = ["你是一個 helpful 的助理，請用繁體中文回答。以下是過去對話："]
        for m in history:
            prefix = "使用者" if m["role"] == "user" else "助理"
            lines.append(f"{prefix}：{m['text']}")
        return "\n".join(lines)

    with st.chat_message("assistant"):
        with st.spinner("思考中…"):
            prompt = build_prompt(st.session_state.history)
            resp = client.models.generate_content(model=MODEL, contents=prompt)
            reply = (getattr(resp, "text", "") or "").strip() or "(沒有回應內容)"
            st.markdown(reply)

    st.session_state.history.append({"role": "assistant", "text": reply})
