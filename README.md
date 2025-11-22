# AutoAgent — Research & Insights (Streamlit)

**Project:** AutoAgent — Research & Insights Agent  
**Goal:** Given a topic, the agent fetches web content, summarizes key points, and uses Gemini to generate trend predictions and actionable insights. The app is deployable on Streamlit Cloud.

## Features
- Streamlit UI with simple inputs and progress feedback.
- Web scraping using `requests` + `BeautifulSoup`.
- Gemini API integration (using `google-genai` client or REST).
- Visual charts with Plotly and pandas.
- Exportable PDF/Markdown report (basic).
- Beginner-friendly structure for hackathon judges.

## Setup
1. Copy `.env.example` to `.env` and set `GEMINI_API_KEY`.
2. Create virtualenv and install:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Run the app:
```bash
streamlit run app.py
```

## Gemini API notes
This starter uses the official Gemini/GenAI client (recommended) or REST. See the official docs for examples and model choices. Examples and quickstarts: Google AI docs.  
(Official docs: https://ai.google.dev/api, https://ai.google.dev/gemini-api/docs/quickstart).  

## Files
- `app.py` — Streamlit UI and orchestration
- `gen_ai.py` — Gemini client wrapper (reads GEMINI_API_KEY from env)
- `scraper.py` — web scraping helpers (requests + BS4)
- `utils.py` — helpers for cleaning and summarizing
- `resume/` — standout resume in Markdown + PDF

## Deploy
- Push to GitHub and connect to Streamlit Cloud.
- Set the environment variable `GEMINI_API_KEY` in the Streamlit app settings.

