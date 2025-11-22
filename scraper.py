# scraper.py
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    "User-Agent": os.getenv("USER_AGENT", "AutoAgentHackathon/1.0")
}


def _try_fetch_from_ddg(query: str, max_pages: int = 1):
    """
    Internal helper: tries to fetch search results from DuckDuckGo HTML.
    May return an empty list if blocked or HTML structure changed.
    """
    snippets = []
    try:
        for page in range(max_pages):
            params = {"q": query, "s": str(page * 10)}
            r = requests.get(
                "https://duckduckgo.com/html/",
                params=params,
                headers=HEADERS,
                timeout=10,
            )
            if r.status_code != 200:
                break

            soup = BeautifulSoup(r.text, "html.parser")
            results = soup.find_all("a", {"class": "result__a"})
            summaries = soup.find_all("a", {"class": "result__snippet"})

            if not results:
                break

            for i, a in enumerate(results):
                title = a.get_text(strip=True)
                snippet = (
                    summaries[i].get_text(strip=True)
                    if i < len(summaries)
                    else ""
                )
                snippets.append(
                    {
                        "title": title or f"Result {i+1}",
                        "snippet": snippet or f"Snippet for {query}",
                    }
                )
    except Exception as e:
        # For debugging (you can print this in terminal if needed)
        print("[scraper] error:", e)

    return snippets


def fetch_search_snippets(query: str, max_pages: int = 1):
    """
    Public function used by the app.
    - Tries real web scraping.
    - If nothing is found (blocked / offline), returns synthetic snippets
      so that the rest of the pipeline still works for demo purposes.
    """
    snippets = _try_fetch_from_ddg(query, max_pages=max_pages)

    if snippets:
        return snippets

    # --- Fallback: synthetic snippets so demo always works ---
    fallback = [
        {
            "title": f"Overview of {query}",
            "snippet": f"{query} is an emerging area where AI agents are used to solve real-world problems.",
        },
        {
            "title": f"Applications of {query}",
            "snippet": f"Common applications of {query} include automation, decision support, and personalised user experiences.",
        },
        {
            "title": f"Challenges in {query}",
            "snippet": f"Key challenges in {query} involve data quality, scalability, safety, and ethical considerations.",
        },
        {
            "title": f"Future of {query}",
            "snippet": f"Future trends in {query} point towards more autonomy, better collaboration between agents, and tighter integration with existing systems.",
        },
    ]
    return fallback
