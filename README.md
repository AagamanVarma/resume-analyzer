# Resume Analyzer (Flask + Gemini AI)

This is a web application that analyzes resumes uploaded in PDF format and provides detailed feedback powered by Google Gemini AI. It extracts named entities, identifies technical skills, summarizes experience-related content, and offers intelligent improvement suggestions to help optimize your resume for job applications.

## Features

- Upload and parse PDF resumes
- Extract named entities using spaCy NLP
- Detect technical and soft skills using PhraseMatcher
- Summarize experience-related content from the resume
- Generate AI-powered feedback and suggestions using Gemini API
- Clean and simple web interface with Flask

## Technologies Used

- Python
- Flask
- spaCy (`en_core_web_sm`)
- Google Generative AI (Gemini 2.5 Pro)
- PyMuPDF (`fitz`)
- HTML + Jinja templates

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/resume-analyzer-flask.git
cd resume-analyzer-flask
