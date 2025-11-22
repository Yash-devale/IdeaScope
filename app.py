# app.py
import streamlit as st
from gen_ai import GeminiClient
from scraper import fetch_search_snippets
from utils import summarize_text, make_dataframe, build_report

st.set_page_config(
    page_title="IdeaScope – AI Research & Insights",
    layout="wide"
)

st.title("🧠 IdeaScope – AI Research & Insights Agent")
st.caption("Give me a topic. I’ll research the web, summarise it, and (optionally) ask Gemini for trends & insights.")

# --- Sidebar: status & options ---
with st.sidebar:
    st.header("⚙️ Settings")
    st.write("This app **never asks for your API key in the UI**.")
    st.write("It reads `GEMINI_API_KEY` from your environment / `.env` file.")

    gemini_client = GeminiClient()
    if gemini_client.enabled:
        st.success("Gemini status: ✅ Enabled")
    else:
        st.warning(
            "Gemini status: ❌ Disabled\n\n"
            "Set GEMINI_API_KEY in your environment to enable predictions."
        )

    depth = st.slider("Scrape depth (pages)", 1, 5, 2)
    st.markdown("---")
    st.markdown("**Quick topics:**")
    quick = st.radio(
        "Pick a sample topic (optional):",
        [
            "AI agents for education and personalised learning",
            "Autonomous AI agents in software development",
            "AI agents for environmental monitoring",
            "Custom… (type your own below)"
        ],
        index=0
    )

# --- Main input ---
default_text = (
    "AI agents for education and personalised learning"
    if not "Custom…" in quick
    else ""
)

topic = st.text_input("🔍 Topic to explore", value=default_text, max_chars=200)

col_run, col_clear = st.columns([2, 1])
run_clicked = col_run.button("🚀 Run Research")
if col_clear.button("Clear"):
    st.experimental_rerun()

# --- Main logic ---
if run_clicked:
    if not topic.strip():
        st.error("Please enter a topic first.")
    else:
        with st.spinner("Fetching web snippets…"):
            snippets = fetch_search_snippets(topic, max_pages=depth)

        if not snippets:
            st.error("No snippets found. Try a different topic or reduce depth.")
        else:
            st.success(f"Fetched {len(snippets)} snippets from the web.")

            # Layout: 2 columns
            col_left, col_right = st.columns([2, 1])

            # LEFT: summary + predictions
            with col_left:
                st.subheader("📚 Summary of what the web says")
                combined = "\n\n".join(s["snippet"] for s in snippets if s["snippet"])
                summary = summarize_text(combined)
                st.write(summary)

                st.subheader("🔮 Predictions & insights (Gemini)")
                if gemini_client.enabled:
                    prompt = (
                        "You are an expert analyst. Based on the following summary, "
                        "give:\n"
                        "1) Three short trend predictions\n"
                        "2) Three actionable insights\n\n"
                        f"Summary:\n{summary}"
                    )
                    predictions = gemini_client.predict(prompt)
                    st.write(predictions)
                else:
                    predictions = "[Gemini disabled] Only summary is available."
                    st.info(predictions)

            # RIGHT: raw data + table + export
            with col_right:
                st.subheader("🧩 Snippet samples")
                for s in snippets[:5]:
                    st.markdown(f"**{s['title']}**")
                    st.caption(s["snippet"])
                    st.markdown("---")

                st.subheader("📊 All snippets table")
                df = make_dataframe(snippets)
                st.dataframe(df, use_container_width=True)

                st.subheader("📥 Export report")
                report_md = build_report(topic, summary, predictions, snippets[:10])
                st.download_button(
                    "Download report (Markdown)",
                    data=report_md,
                    file_name=f"report_{topic.replace(' ', '_')}.md",
                    mime="text/markdown",
                )

else:
    st.info(
        "👆 Enter a topic above and click **Run Research**.\n\n"
        "Tip for hackathon: try topics like "
        "**'Autonomous multi-agent systems for real-world problem solving'**."
    )
