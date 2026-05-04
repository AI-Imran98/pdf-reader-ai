import streamlit as st
from google import genai
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Page config
st.set_page_config(
    page_title="PDF Reader AI",
    page_icon="📄",
    layout="centered"
)

# Title
st.title("📄 PDF Reader AI")
st.subheader("যেকোনো PDF থেকে প্রশ্ন করুন!")

# PDF read function
def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# AI question function
def ask_question(pdf_text, question):
    prompt = f"""
    তুমি একজন AI Assistant।
    শুধুমাত্র নিচের PDF এর তথ্য থেকে উত্তর দাও।
    PDF এ না থাকলে বলো "এই তথ্য PDF এ নেই"।
    বাংলায় উত্তর দাও।

    PDF তথ্য:
    {pdf_text}

    প্রশ্ন: {question}
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text

# Upload PDF
uploaded_file = st.file_uploader(
    "PDF আপলোড করুন",
    type="pdf"
)

if uploaded_file is not None:
    # Read PDF
    with st.spinner("PDF পড়া হচ্ছে..."):
        pdf_text = read_pdf(uploaded_file)
    
    st.success(f"✅ PDF পড়া হয়েছে!")

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])

    # Question input
    question = st.chat_input("প্রশ্ন করুন...")

    if question:
        # Show user question
        st.chat_message("user").write(question)
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        # Get AI answer
        with st.spinner("AI উত্তর দিচ্ছে..."):
            answer = ask_question(pdf_text, question)

        # Show answer
        st.chat_message("assistant").write(answer)
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

else:
    st.info("👆 উপরে PDF আপলোড করুন")
    st.markdown("""
    ### কীভাবে ব্যবহার করবেন:
    1. 📤 যেকোনো PDF আপলোড করুন
    2. ❓ প্রশ্ন করুন
    3. 🤖 AI উত্তর দেবে!
    """)