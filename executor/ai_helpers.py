# executor/ai_helpers.py
import google.generativeai as genai
from decouple import config

# ✅ Set your Gemini API key from .env
genai.configure(api_key=config("GEMINI_API_KEY"))

def generate_hint(prompt):
    try:
        # ✅ Use correct Gemini model
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini Error: {str(e)}"
