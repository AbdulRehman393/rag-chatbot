import os
import requests
import streamlit as st


from dotenv import load_dotenv
load_dotenv()


API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="LangChain RAG Chatbot", page_icon="🤖")
st.title("LangChain RAG Chatbot")

# Sidebar: file ingestion
st.sidebar.header("📄 Ingest documents")
uploaded = st.sidebar.file_uploader("Upload PDF/TXT/MD", type=["pdf", "txt", "md"])
if uploaded and st.sidebar.button("Index file"):
    with st.spinner("Indexing..."):
        files = {"upload": (uploaded.name, uploaded.getvalue())}
        r = requests.post(f"{API_URL}/ingest", files=files)
        if r.ok:
            st.sidebar.success(f"Indexed {r.json()['chunks_indexed']} chunks ✅")
        else:
            st.sidebar.error(r.text)

# Chat state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for role, content in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(content)

# Chat input
q = st.chat_input("Ask something about your documents...")
if q:
    st.session_state.messages.append(("user", q))
    with st.chat_message("user"):
        st.markdown(q)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            payload = {"question": q, "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini")}
            r = requests.post(f"{API_URL}/chat", json=payload)
            if r.ok:
                ans = r.json()["answer"]
                st.markdown(ans)
                st.session_state.messages.append(("assistant", ans))
            else:
                st.error(r.text)