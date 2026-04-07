import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # Load the Gemini API key from .env.
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


def _generate_text(prompt: str, action: str) -> str:
    """Send a prompt to Gemini and return cleaned text."""
    gemini_model = _require_model()

    try:
        response = gemini_model.generate_content(prompt)
    except Exception as e:
        raise RuntimeError(f"Gemini API error while {action}: {str(e)}") from e

    if response.text and response.text.strip():
        return response.text.strip()

    raise RuntimeError(f"Gemini returned no response while {action}.")


def get_resume_feedback(text):
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

    return _generate_text(prompt, "generating resume feedback")



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

    response_text = _generate_text(prompt, "extracting skills from the job description")
    skills = [skill.strip() for skill in response_text.split(",")]
    return [skill for skill in skills if skill]