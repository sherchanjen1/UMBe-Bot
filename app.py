import streamlit as st
from chatbot import ask_umassbot

st.set_page_config(page_title="UMBeBot", page_icon="🧠")

st.markdown("""
<style>
.user-bubble {
    background-color: #DCF8C6;
    color: black;
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 5px;
    max-width: 80%;
    align-self: flex-end;
}
.bot-bubble {
    background-color: #F1F0F0;
    color: black;
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 10px;
    max-width: 80%;
    align-self: flex-start;
}
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 10px;
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 UMBeBot – Your UMass Boston AI Assistant")

# Fixed course for now
course = "AI for All"

# Instructor modules
modules = [
    "Cody Turner", "Shirley Tang", "Jacob Adamczyk", "Mentor Prof Matthew Davis",
    "Mentor Prof Yinxin Wan", "Mentor Prof. Shcihao Pei", "Ping Chen", "Prof fusheng wang from stony brook university"
]
module = st.sidebar.selectbox("Select Module (Instructor):", modules)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input (auto-submit on Enter)
with st.form("chat_form", clear_on_submit=True):
    query = st.text_input("Ask your course-related question...", placeholder="e.g., What was the Shark Tank assignment?")
    submitted = st.form_submit_button("Ask")

if submitted and query.strip():
    with st.spinner("UMBeBot is thinking..."):
        response = ask_umassbot(query, course=course, module=module)
    st.session_state.messages.append({"user": query, "bot": response})
    st.rerun()

# Display chat messages
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    st.markdown(f"<div class='user-bubble'><strong>You:</strong> {msg['user']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='bot-bubble'><strong>UMBeBot:</strong> {msg['bot']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
