 # Resume Analyzer (Flask + Gemini AI)

**Resume Analyzer** is a web-based application that analyzes resumes uploaded in PDF format and provides detailed, AI-powered feedback. The system leverages natural language processing (NLP) and Google Gemini AI to extract relevant information, identify technical skills, summarize experience, and generate personalized suggestions to improve the quality and effectiveness of the resume.

---

## Features

* Upload and process resumes in PDF format
* Extract named entities using spaCy NLP
* Identify technical and soft skills with PhraseMatcher
* Summarize experience-related sections
* Generate feedback and improvement suggestions using Gemini AI
* Minimal and clean user interface using Flask and Jinja templates

---

## Technologies Used

* Python
* Flask
* spaCy (`en_core_web_sm`)
* Google Generative AI (Gemini 2.5 Pro)
* PyMuPDF (`fitz`)
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

If `requirements.txt` is missing, install manually:

```bash
pip install flask spacy PyMuPDF google-generativeai
python -m spacy download en_core_web_sm
```

### 4. Set Up the API Key

Create a `.env` file in the project root and add your Gemini API key:

```
GOOGLE_API_KEY=your_api_key_here
```

You can obtain your API key from: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

### 5. Run the Application

```bash
python app.py
```

Access the application in your browser at: `http://127.0.0.1:5000`

---

 
## Future Enhancements

* Deploy to a public hosting platform (e.g., Render, Railway, or Vercel)
* Implement user authentication and resume history
* Add resume scoring and benchmarking features
* Provide job recommendations based on skillset analysis

---

## Contact

For any suggestions, improvements, or collaboration inquiries, feel free to open an issue or connect via LinkedIn.

---

