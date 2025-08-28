# # import google.generativeai as genai
# # import os

# # # Set Gemini API key
# # genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # def get_resume_feedback(resume_text):
# #     model = genai.GenerativeModel("gemini-pro")

# #     prompt = f"""
# #     You are a professional resume reviewer. Based on the following resume content, provide:
# #     1. Suggested improvements (skills, formatting, grammar, etc.)
# #     2. Summary of strengths
# #     3. Missing or weak sections

# #     Resume Text:
# #     \"\"\"
# #     {resume_text}
# #     \"\"\"
# #     ""
# #     response = model.generate_content(prompt)
# #     return response.text
# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# load_dotenv()  # Load variables from .env

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# model = genai.GenerativeModel("gemini-1.5-pro")

# def get_resume_feedback(text):
#     prompt = f"Give feedback on this resume:\n{text}"
#     response = model.generate_content(prompt)
#     return response.text

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # Load API key from .env file
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-pro")  # or "gemini-pro" if that works for you

def get_resume_feedback(text):
    prompt = f"""
    You are a professional resume reviewer.
    Please provide feedback in bullet points about:
    - Strengths
    - Weaknesses
    - Suggestions for improvement

    Resume:
    \"\"\"
    {text}
    \"\"\"
    """

    try:
        response = model.generate_content(prompt)

        # ✅ Safe access — check if parts exist
        if response.parts and len(response.parts) > 0:
            return response.text.strip()
        else:
            return "⚠️ Gemini returned no response. Try reducing resume length or improving formatting."
    
    except Exception as e:
        # ✅ Handle API errors gracefully
        return f"⚠️ Gemini API error: {str(e)}"
