import fitz
import markdown2
import spacy
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from spacy.matcher import PhraseMatcher

from gemini_suggester import extract_skills_from_jd, get_resume_feedback

app = FastAPI(title="Resume Analyzer")
templates = Jinja2Templates(directory="templates")

nlp = spacy.load("en_core_web_sm")


def analyze_resume(text, skills_to_find, matcher_instance):
    # Parse the resume text once so we can reuse the tokens, sentences, and entities.
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Collect matched skills from the PhraseMatcher.
    matches = matcher_instance(doc)
    skills = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        skills.add(span.text)

    # Keep simple evidence of experience-related content for the report.
    experience_sentences = [sent.text for sent in doc.sents if "experience" in sent.text.lower()]

    # Simple score: skill match contributes most, and experience mentions add a small bonus.
    total_skills = len(skills_to_find)
    matched_skills = len(skills)
    skill_match_percentage = (matched_skills / total_skills) * 100 if total_skills > 0 else 0

    score = int(skill_match_percentage * 0.6 + len(experience_sentences) * 10)

    return {
        "entities": entities,
        "skills": sorted(skills),
        "experience_summary": experience_sentences,
        "skill_match_percentage": round(skill_match_percentage, 2),
        "score": min(score, 100)  # Max 100
    }


def extract_text_from_pdf(pdf_bytes):
    # PyMuPDF can read directly from bytes, so we do not need to save uploads to disk.
    text = ""
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def upload(
    request: Request,
    resume: UploadFile = File(...),
    job_description: str = Form(...),
):
    if not resume.filename:
        raise HTTPException(status_code=400, detail="No selected file")

    # Basic validation keeps the endpoint predictable for users.
    if job_description.strip() == "":
        raise HTTPException(status_code=400, detail="Empty job description")

    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF resume")

    try:
        resume_bytes = await resume.read()
        resume_text = extract_text_from_pdf(resume_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract PDF text: {e}")

    # Gemini must provide the skill list; if it fails, we return a clear error instead of guessing.
    try:
        dynamic_skills_list = extract_skills_from_jd(job_description)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp(skill.lower()) for skill in dynamic_skills_list]
    matcher.add("SKILLS", patterns)

    analysis = analyze_resume(resume_text, dynamic_skills_list, matcher)

    # Gemini feedback is required for this page; if it fails, return a clean service error.
    try:
        raw_suggestions = get_resume_feedback(resume_text)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))

    suggestions_html = markdown2.markdown(raw_suggestions)

    chart_data = {
        "skill_match_percentage": analysis["skill_match_percentage"],
        "score": analysis["score"],
        "matched_skills": len(analysis["skills"]),
        "total_skills": len(dynamic_skills_list),
    }

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "analysis": analysis,
            "suggestions": suggestions_html,
            "chart_data": chart_data,
        },
    )
