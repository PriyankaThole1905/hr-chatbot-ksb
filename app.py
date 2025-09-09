import streamlit as st
from utils.chatbot import generate_response
from utils.faq_loader import load_faqs
from utils.safety_loader import load_safety_info
from PIL import Image
from langchain_community.embeddings import SentenceTransformerEmbeddings


# Page Config
st.set_page_config(page_title="🤖 HR Chatbot", layout="centered")

# Header & Logo
col1, col2 = st.columns([1, 4])
with col1:
    logo = Image.open("data/ksb_logo.png")  # Make sure this file exists
    st.image(logo, width=80)
with col2:
    st.title("🤖 HR Chatbot")
    st.markdown("### Welcome to the 💼 KSB Tech HR Assistant")

st.divider()

# Interactive Button Navigation
st.markdown("#### 🧭 Select a section to continue:")
col_chat, col_faq, col_safety = st.columns(3)

# Session State for Navigation
if "section" not in st.session_state:
    st.session_state.section = "Chatbot"

# Button Navigation Handling
with col_chat:
    if st.button("🎯 Chatbot"):
        st.session_state.section = "Chatbot"

with col_faq:
    if st.button("📚 FAQ"):
        st.session_state.section = "FAQ"

with col_safety:
    if st.button("🛡️ Women Safety"):
        st.session_state.section = "Women Safety"

st.divider()

# Section Rendering
if st.session_state.section == "Chatbot":
    st.subheader("💬 Ask Me Anything about HR 📄")
    query = st.text_input("🔍 Enter your HR query below:")
    if query:
        with st.spinner("🤖 Thinking..."):
            answer = generate_response(query)
            st.success(f"📝 Answer: {answer}")

elif st.session_state.section == "FAQ":
    st.subheader("📚 Frequently Asked Questions")
    faqs = load_faqs()
    for item in faqs:
        with st.expander(f"❓ {item['question']}"):
            st.write(f"💡 {item['answer']}")

elif st.session_state.section == "Women Safety":
    st.subheader("🛡️ Women Safety Guidelines")
    try:
        safety_info = load_safety_info()
        st.markdown("Here are the policies in place to ensure the safety and well-being of women at KSB Tech.")
        for item in safety_info:
            st.markdown(f"**📌 {item['category']}**: {item['detail']}")
    except Exception as e:
        st.error(f"❗Error loading safety info: {e}")

# Footer
st.divider()
st.markdown("💙 Made with love by KSB Tech IT Team 😄")
