import textwrap
import pandas as pd

def summarize_text(text: str, max_sentences: int = 5) -> str:
    # Naive summarizer: split into sentences and return first N. Replace with LLM summary for better results.
    import re
    sents = re.split(r'(?<=[.!?])\s+', text.strip())
    if not sents:
        return ''
    summary = ' '.join(sents[:max_sentences])
    return summary

def make_dataframe(snippets):
    import pandas as pd
    return pd.DataFrame(snippets)

def build_report(topic, summary, predictions, snippets):
    md = []
    md.append(f"# Research report — {topic}\n")
    md.append("## Summary\n")
    md.append(summary + "\n")
    md.append("## Predictions & Insights\n")
    md.append(predictions + "\n")
    md.append("## Top snippets\n")
    for s in snippets:
        md.append(f"- **{s['title']}**: {s['snippet']}\n")
    return '\n'.join(md)
