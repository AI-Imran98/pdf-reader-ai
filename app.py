from google import genai
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

# API Key লোড করা
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# PDF পড়া
def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# AI কে প্রশ্ন করা
def ask_question(pdf_text, question):
    prompt = f"""
    তুমি একজন বাংলা ভাষার AI Assistant।
    শুধুমাত্র নিচের PDF এর তথ্য থেকে উত্তর দাও।
    PDF এ না থাকলে বলো "এই তথ্য PDF এ নেই"।
    সবসময় বাংলায় উত্তর দাও।

    PDF তথ্য:
    {pdf_text}

    প্রশ্ন: {question}
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text

# Main Program
print("=== PDF Reader AI ===")
pdf_path = input("PDF এর নাম লিখুন: ")
pdf_text = read_pdf(pdf_path)
print("✅ PDF পড়া হয়েছে!")

while True:
    question = input("\nপ্রশ্ন করুন (বের হতে 'exit' লিখুন): ")
    if question == "exit":
        break
    answer = ask_question(pdf_text, question)
    print(f"\n🤖 উত্তর: {answer}")
