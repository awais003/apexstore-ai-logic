import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 1. Load the secret key
load_dotenv()

# 2. Initialize the Brain (Gemini 1.5 Flash is great for speed/cost)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# 3. Test the connection
try:
    response = llm.invoke("System check: Are you online?")
    print("\n✅ Brain Status: ONLINE")
    print(f"✅ Gemini Response: {response.content}")
except Exception as e:
    print(f"\n❌ Connection Failed: {e}")
