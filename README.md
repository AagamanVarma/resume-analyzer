# Resume Analyzer (FastAPI + Gemini AI)

**Resume Analyzer** is a web-based application that analyzes resumes uploaded in PDF format and provides detailed, AI-powered feedback. The system leverages natural language processing (NLP), FastAPI, and Google Gemini AI to extract relevant information, identify technical skills, summarize experience, and generate personalized suggestions to improve the quality and effectiveness of the resume.

---

## Features

* Upload and process resumes in PDF format
* Extract named entities using spaCy NLP
* Identify technical and soft skills with PhraseMatcher
* Summarize experience-related sections
* Generate feedback and improvement suggestions using Gemini AI
* Minimal and clean user interface using FastAPI and Jinja templates

---

## Technologies Used

* Python
* FastAPI
* spaCy (`en_core_web_sm`)
* Google Generative AI (Gemini 2.5 Flash)
* PyMuPDF (`fitz`)
* Uvicorn
* HTML and Jinja for templating

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/AagamanVarma/resume-analyzer.git
cd resume-analyzer
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # for macOS/Linux
venv\Scripts\activate     # for Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```


### 4. Set Up the API Key

Create a `.env` file in the project root and add your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

You can obtain your API key from: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

### 5. Run the Application

```bash
uvicorn app:app --reload
```

Access the application in your browser at: `http://127.0.0.1:8000`

---



