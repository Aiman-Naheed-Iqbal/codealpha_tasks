import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from src.chatbot import ChatBot

# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="AI ChatBot",
    page_icon="🤖",
    layout="wide"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
/* Background */
.stApp {
    background-color: #0f172a;
}

/* Chat container */
.chat-container {
    max-width: 800px;
    margin: auto;
}

/* Chat bubbles */
.user-bubble {
    background-color: #2563eb;
    color: white;
    padding: 12px 16px;
    border-radius: 12px;
    margin: 8px 0;
    text-align: right;
}

.bot-bubble {
    background-color: #1e293b;
    color: #e2e8f0;
    padding: 12px 16px;
    border-radius: 12px;
    margin: 8px 0;
    text-align: left;
}

/* Input box */
.stTextInput>div>div>input {
    background-color: #1e293b;
    color: white;
    border-radius: 10px;
}

/* Buttons */
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    padding: 6px 16px;
}

/* Title */
.title {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    color: white;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.title("⚙️ Settings")
    st.write("Customize your chatbot")

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []

    st.markdown("---")
    st.write("### 📌 About")
    st.write("This chatbot uses TF-IDF + Cosine Similarity.")

# -------------------- MAIN UI --------------------
st.markdown('<div class="title">🤖 AI Chat Assistant</div>', unsafe_allow_html=True)

bot = ChatBot()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat history
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(f'<div class="user-bubble">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">{msg}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------- INPUT AREA --------------------
col1, col2 = st.columns([6, 1])

with col1:
    user_input = st.text_input("Type your message...", label_visibility="collapsed")

with col2:
    send = st.button("Send")

# -------------------- CHAT LOGIC --------------------
if send and user_input:
    response = bot.get_response(user_input)

    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("bot", response))

    st.rerun()