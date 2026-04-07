import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # Load API key from .env file
api_key = os.getenv("GEMINI_API_KEY")


def _get_model():
    if not api_key:
        return None

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


model = _get_model()


def _require_model():
    if model is None:
        raise RuntimeError(
            "GEMINI_API_KEY is missing or Gemini could not be initialized. "
            "Add a valid key to your .env file."
        )
    return model


def get_resume_feedback(text):
    gemini_model = _require_model()

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
        response = gemini_model.generate_content(prompt)

        if response.parts and len(response.parts) > 0:
            return response.text.strip()
        else:
            raise RuntimeError("Gemini returned no response for resume feedback.")

    except Exception as e:
        raise RuntimeError(f"Gemini API error while generating resume feedback: {str(e)}") from e



def extract_skills_from_jd(job_description_text):
    """Extracts key skills from a job description using the Gemini API."""
    gemini_model = _require_model()

    prompt = f"""
    Based on the following job description, please extract all the important technical skills, soft skills, and tools.
    Return them as a single comma-separated list. For example: Python,Java,SQL,Teamwork,Project Management,AWS,Docker

    Job Description:
    \"\"\"
    {job_description_text}
    \"\"\"
    """

    try:
        response = gemini_model.generate_content(prompt)

        if response.parts and len(response.parts) > 0:
            skills = [skill.strip() for skill in response.text.split(',')]
            return [skill for skill in skills if skill]
        else:
            raise RuntimeError("Gemini returned no response while extracting skills from the job description.")

    except Exception as e:
        raise RuntimeError(f"Gemini API error while extracting skills: {str(e)}") from e