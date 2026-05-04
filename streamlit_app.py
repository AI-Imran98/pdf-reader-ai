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
st.subheader("Ask any question from your PDF instantly!")

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
    You are a helpful AI Assistant.
    Answer questions ONLY from the PDF content below.
    If the answer is not in the PDF, say 
    "This information is not available in the PDF."
    Always answer in English clearly and concisely.

    PDF Content:
    {pdf_text}

    Question: {question}
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload your PDF file",
    type="pdf"
)

if uploaded_file is not None:
    # Read PDF
    with st.spinner("Reading PDF..."):
        pdf_text = read_pdf(uploaded_file)

    st.success(f"✅ PDF loaded successfully!")

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
    question = st.chat_input("Ask a question about your PDF...")

    if question:
        # Show user question
        st.chat_message("user").write(question)
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        # Get AI answer
        with st.spinner("AI is thinking..."):
            answer = ask_question(pdf_text, question)

        # Show answer
        st.chat_message("assistant").write(answer)
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

else:
    st.info("👆 Please upload a PDF file to get started")
    st.markdown("""
    ### How to use:
    1. 📤 Upload any PDF document
    2. ❓ Ask any question about the PDF
    3. 🤖 Get instant AI-powered answers!
    """)