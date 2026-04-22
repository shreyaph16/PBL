import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print(f"Testing with key starting with: {api_key[:10]}...")

try:
    llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", google_api_key=api_key)
    response = llm.invoke("Hi")
    print("Success!")
    print(response.content)
except Exception as e:
    print(f"Error type: {type(e)}")
    print(f"Error message: {e}")
