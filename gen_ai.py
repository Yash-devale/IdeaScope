# gen_ai.py
import os
from dotenv import load_dotenv

load_dotenv()  # loads GEMINI_API_KEY from .env if present

try:
    from google import genai
    HAS_GENAI_SDK = True
except Exception:
    HAS_GENAI_SDK = False


class GeminiClient:
    """
    Simple wrapper around the Google GenAI SDK.
    - Does NOT ask user for API key.
    - Reads GEMINI_API_KEY from environment/.env.
    - If not available, it runs in "disabled" mode and returns a message.
    """

    def __init__(self):
        self.api_key = os.getenv("AIzaSyB7YjKHLX8CpJgWzo9PQXnKWtzY3r9XzRo")
        self.client = None
        if HAS_GENAI_SDK and self.api_key:
            # The client automatically uses the API key passed here
            # Docs: https://ai.google.dev/gemini-api/docs/quickstart
            self.client = genai.Client(api_key=self.api_key)

    @property
    def enabled(self) -> bool:
        return self.client is not None

    def predict(self, prompt: str, model: str = "gemini-2.5-flash") -> str:
        """
        Generate a response using Gemini.
        Returns a friendly message if Gemini is not enabled.
        """
        if not self.enabled:
            return (
                "[Gemini disabled] Install `google-genai` and set GEMINI_API_KEY "
                "in your environment to enable predictions."
            )

        try:
            response = self.client.models.generate_content(
                model=model,
                contents=prompt
            )
            # New SDK exposes .text for the main output
            return getattr(response, "text", str(response))
        except Exception as e:
            return f"[Gemini error] {e}"
