import google.generativeai as genai
from config import Config
from utils.genai_utils import generate_text

genai.configure(api_key=Config.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# utils/genai_utils.py

def generate_text(prompt):
    return f"AI Generated Content for: {prompt}"