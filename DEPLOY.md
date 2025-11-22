# Deploying to Streamlit Cloud

1. Push this repo to GitHub.
2. Go to https://share.streamlit.io and click 'New app'.
3. Select your GitHub repo and the branch, and set the file path to `app.py`.
4. In the app settings, set environment variables:
   - GEMINI_API_KEY: your_gemini_api_key
   - USER_AGENT: AutoAgent/1.0
5. Deploy. The app will run and you can share the link.

Security note: never commit your API key to the repo. Use env variables in Streamlit or GitHub Secrets.
