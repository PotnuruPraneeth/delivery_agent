import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

print("Attempting to configure Gemini API...")

try:
    # 1. Check if the key is being loaded
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in environment variables.")
        print("Please check your .env file.")
    else:
        print("API Key loaded successfully.")
        genai.configure(api_key=api_key)
        
        # 2. Try to make a simple API call
        print("Initializing model...")
        model = genai.GenerativeModel('gemini-flash-latest')
        
        print("Sending a test prompt to Gemini...")
        response = model.generate_content("This is a test.")
        
        print("\n--- SUCCESS ---")
        print("Gemini Response:", response.text)

except Exception as e:
    print("\n--- AN ERROR OCCURRED ---")
    print(f"The error is: {e}")