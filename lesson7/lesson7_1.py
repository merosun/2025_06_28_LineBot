import os
import streamlit as st
from google import genai
from google.genai import types
import inspect; print(inspect.signature(types.Part.from_text))

st.set_page_config(page_title="Gemini Chat", page_icon="💬")
API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"

if not API_KEY:
    st.error("請先設定 GEMINI_API_KEY 環境變數")
    st.stop()

client = genai.Client(api_key=API_KEY)

if "history" not in st.session_state:
    st.session_state.history = []

st.title("💬 Gemini Chat（繁體中文）")

for m in st.session_state.history:
    with st.chat_message("user" if m["role"] == "user" else "assistant"):
        st.markdown(m["text"])

uploaded_files = st.file_uploader(
    "（選填）上傳圖片：支援 jpg/png/webp",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

if uploaded_files:
    cols = st.columns(min(3, len(uploaded_files)))
    for i, f in enumerate(uploaded_files):
        with cols[i % len(cols)]:
            st.image(f, caption=f.name, use_container_width=True)

user_input = st.chat_input("輸入你的問題…（可先選圖片再提問）")

if user_input or uploaded_files:
    display_text = user_input if user_input else "(無文字)"
    if uploaded_files:
        display_text += f"\n（附 {len(uploaded_files)} 張圖片）"
    st.session_state.history.append({"role": "user", "text": display_text})

    with st.chat_message("user"):
        st.markdown(display_text)

    def build_prompt(history):
        lines = ["你是一個股市財經專家，請用繁體中文回答。以下是過去對話："]
        for m in history:
            prefix = "使用者" if m["role"] == "user" else "助理"
            lines.append(f"{prefix}：{m['text']}")
        return "\n".join(lines)

    with st.chat_message("assistant"):
        try:
            prompt_text = build_prompt(st.session_state.history)

            parts = []
            if uploaded_files:
                for f in uploaded_files:
                    try:
                        img_bytes = f.getvalue()
                    except Exception:
                        f.seek(0)
                        img_bytes = f.read()

                    suffix = os.path.splitext(f.name)[1].lower()
                    if suffix in (".jpg", ".jpeg"):
                        mime = "image/jpeg"
                    elif suffix == ".png":
                        mime = "image/png"
                    elif suffix == ".webp":
                        mime = "image/webp"
                    else:
                        mime = "application/octet-stream"

                    parts.append(types.Part.from_bytes(data=img_bytes, mime_type=mime))

            # 文字一定要用 keyword 參數
            parts.append(types.Part.from_text(text=prompt_text))

            resp = client.models.generate_content(
                model=MODEL,
                contents=types.Content(role="user", parts=parts),
                config=types.GenerateContentConfig(
                    temperature=0.5,
                    top_p=0.9,
                    max_output_tokens=512,
                ),
            )

            reply = (getattr(resp, "text", "") or "").strip()
            if not reply and getattr(resp, "candidates", None):
                for c in resp.candidates:
                    if getattr(c, "content", None):
                        for p in getattr(c.content, "parts", []) or []:
                            if getattr(p, "text", None):
                                reply = p.text.strip()
                                if reply:
                                    break
                    if reply:
                        break
            if not reply and getattr(resp, "prompt_feedback", None):
                reply = f"(沒有文字回應，可能被過濾或無法產生。feedback={resp.prompt_feedback})"

            reply = reply or "(沒有回應內容)"

        except Exception as e:
            st.error("呼叫 generate_content 發生錯誤")
            st.exception(e)
            reply = f"(發生錯誤：{e})"

        st.markdown(reply)
        st.session_state.history.append({"role": "assistant", "text": reply})
