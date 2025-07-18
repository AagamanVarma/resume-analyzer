# import google.generativeai as genai
# import os

# # Set Gemini API key
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# def get_resume_feedback(resume_text):
#     model = genai.GenerativeModel("gemini-pro")

#     prompt = f"""
#     You are a professional resume reviewer. Based on the following resume content, provide:
#     1. Suggested improvements (skills, formatting, grammar, etc.)
#     2. Summary of strengths
#     3. Missing or weak sections

#     Resume Text:
#     \"\"\"
#     {resume_text}
#     \"\"\"
#     ""
#     response = model.generate_content(prompt)
#     return response.text
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # Load variables from .env

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-pro")

def get_resume_feedback(text):
    prompt = f"Give feedback on this resume:\n{text}"
    response = model.generate_content(prompt)
    return response.text

