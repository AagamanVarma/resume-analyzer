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
model = genai.GenerativeModel("gemini-2.5-pro")   

# def get_resume_feedback(text):
#     prompt = f"""
#     You are a professional resume reviewer.
#     Please provide feedback in some bullet points about:
#     - Strengths
#     - Weaknesses
#     - Suggestions for improvement

#     Resume:
#     \"\"\"
#     {text}
#     \"\"\"
#     """

#     try:
#         response = model.generate_content(prompt)

#         #  Safe access — check if parts exist
#         if response.parts and len(response.parts) > 0:
#             return response.text.strip()
#         else:
#             return "⚠️ Gemini returned no response. Try reducing resume length or improving formatting."
    
#     except Exception as e:
#         #  Handle API errors gracefully
#         return f"⚠️ Gemini API error: {str(e)}"
# In gemini_suggester.py

def get_resume_feedback(text):
    # This new prompt is much more specific about formatting.
    prompt = f"""
    You are an expert professional resume reviewer.
    Analyze the following resume and provide your feedback using Markdown formatting.

    Structure your response with these exact headings:
    ### Strengths
    ### Weaknesses
    ### Suggestions for Improvement

    Under each heading, list your points as bullets (e.g., "* Your point here").
    Do not write a single, long paragraph.

    Resume:
    \"\"\"
    {text}
    \"\"\"
    """

    try:
        response = model.generate_content(prompt)

        if response.parts and len(response.parts) > 0:
            return response.text.strip()
        else:
            return "⚠️ Gemini returned no response. Try reducing resume length or improving formatting."

    except Exception as e:
        return f"⚠️ Gemini API error: {str(e)}"

# Add this new function to the end of gemini_suggester.py

def extract_skills_from_jd(job_description_text):
    """Extracts key skills from a job description using the Gemini API."""
    prompt = f"""
    Based on the following job description, please extract all the important technical skills, soft skills, and tools.
    Return them as a single comma-separated list. For example: Python,Java,SQL,Teamwork,Project Management,AWS,Docker

    Job Description:
    \"\"\"
    {job_description_text}
    \"\"\"
    """

    try:
        response = model.generate_content(prompt)

        if response.parts and len(response.parts) > 0:
            # Simple parsing: split by comma and strip whitespace from each skill
            skills = [skill.strip() for skill in response.text.split(',')]
            # Filter out any empty strings that might result from the split
            return [skill for skill in skills if skill]
        else:
            return [] # Return empty list if Gemini gives no response

    except Exception as e:
        print(f"⚠️ Gemini API error while extracting skills: {str(e)}")
        return [] # Return empty list on error