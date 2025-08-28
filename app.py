import re
from flask import Flask, render_template, request
import fitz
import os
import spacy
from spacy.matcher import PhraseMatcher
from gemini_suggester import get_resume_feedback

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

nlp = spacy.load("en_core_web_sm")

skills_list = [
    "Python", "Java", "C++", "SQL", "Machine Learning", "Data Analysis",
    "Communication", "Teamwork", "Project Management", "AWS", "Docker",
    "Flask", "Django", "JavaScript", "React", "HTML", "CSS"
]

matcher = PhraseMatcher(nlp.vocab)
patterns = [nlp(skill) for skill in skills_list]
matcher.add("SKILLS", None, *patterns)

def analyze_resume(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    matches = matcher(doc)
    skills = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        skills.add(span.text)

    experience_sentences = [sent.text for sent in doc.sents if "experience" in sent.text.lower()]

    # Calculate Score
    total_skills = len(skills_list)
    matched_skills = len(skills)
    skill_match_percentage = (matched_skills / total_skills) * 100

    # Simple Scoring
    score = int(skill_match_percentage * 0.6 + len(experience_sentences) * 10)

    return {
        "entities": entities,
        "skills": sorted(skills),
        "experience_summary": experience_sentences,
        "skill_match_percentage": round(skill_match_percentage, 2),
        "score": min(score, 100)  # Max 100
    }


def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def clean_markdown(text):

    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'\*\*|__|\*|_', '', text)
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' not in request.files:
        return "No file part", 400

    file = request.files['resume']
    if file.filename == '':
        return "No selected file", 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        text = extract_text_from_pdf(filepath)
    except Exception as e:
        return f"Failed to extract PDF text: {e}", 500

    analysis = analyze_resume(text)

    raw_suggestions = get_resume_feedback(text)
    cleaned_suggestions = clean_markdown(raw_suggestions)

    # Chart Data
    chart_data = {
        "skill_match_percentage": analysis["skill_match_percentage"],
        "score": analysis["score"],
        "matched_skills": len(analysis["skills"]),
        "total_skills": len(skills_list)
    }

    return render_template(
        "result.html",
        analysis=analysis,
        suggestions=cleaned_suggestions,
        chart_data=chart_data
    )

if __name__ == '__main__':
    app.run(debug=True)
