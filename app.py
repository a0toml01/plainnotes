import streamlit as st
from openai import OpenAI
import os
import re

# Get your OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="PlainNotes", page_icon="📝")

st.title("📝 PlainNotes")
st.subheader("Understand your doctor's notes – in plain language")

st.markdown("""
Welcome to **PlainNotes**, a tool that transforms complex clinical notes into easy-to-understand summaries.
Just paste your medical notes below, and we’ll simplify them into plain language and suggest follow-up questions and actions.
""")

# User input for clinical notes
input_notes = st.text_area("Paste your doctor's notes here:", height=200)

# Live character count
char_count = len(input_notes)
st.caption(f"Character count: {char_count}/3000")

if st.button("Translate & Suggest"):
    if not openai_api_key:
        st.error("OpenAI API key not found. Please set your API key in the environment variable 'OPENAI_API_KEY'.")
    elif not input_notes.strip():
        st.warning("Please paste some doctor's notes before submitting.")
    elif len(input_notes.strip()) > 3000:
        st.error("Note is too long. Please shorten the input to under 3000 characters.")
    else:
        client = OpenAI(api_key=openai_api_key)
        with st.spinner("Generating summary and suggestions..."):
            try:
                prompt = (
                    "You are a medical communication assistant. For the following doctor's note, provide:\n"
                    "1. A summary in plain language (6th-8th grade level).\n"
                    "2. A list of suggested follow-up questions the patient might ask.\n"
                    "3. Recommended actions the patient should consider.\n"
                    "4. A glossary explaining any medical terms used.\n\n"
                    f"Doctor's note:\n{input_notes}\n\n"
                    "Plain language summary:"
                )

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You simplify clinical notes into plain language summaries, suggest follow-up questions, recommend actions, and provide a glossary of medical terms."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=800
                )

                summary = response.choices[0].message.content.strip()
                st.markdown("---")

                # Split the response into sections using regex
                sections = re.split(r"(?i)^(plain language summary:|suggested follow-up questions:|recommended actions:|glossary:)", summary, flags=re.MULTILINE)
                section_titles = [
                    ("plain language summary", "📝 Plain Language Summary"),
                    ("suggested follow-up questions", "❓ Suggested Follow-up Questions"),
                    ("recommended actions", "✅ Recommended Actions"),
                    ("glossary", "📚 Glossary")
                ]
                # Build a dict of section title (lowercase) to content
                section_dict = {}
                for i in range(1, len(sections), 2):
                    key = sections[i].strip().lower().rstrip(":")
                    value = sections[i+1].strip() if i+1 < len(sections) else ""
                    section_dict[key] = value

                for key, display_title in section_titles:
                    if key in section_dict and section_dict[key]:
                        st.subheader(display_title)
                        st.markdown(section_dict[key])

                st.success("Your summary and suggestions have been generated.")

            except Exception as e:
                st.error(f"An error occurred while generating the summary: {e}")

st.caption("Note: This tool does not store or transmit any personal health information.")

with st.expander("🔐 Learn more about how we protect your privacy"):
    st.markdown("""
    **PlainNotes is privacy-first by design.**

    - We don’t require you to sign up or create an account.
    - Your notes are **not stored or logged** — once your summary is generated, the text is gone.
    - We use a secure AI model (like OpenAI’s GPT-3.5) to generate summaries, and that’s it.
    - You can remove names or personal details if you prefer — PlainNotes still works.

    **You’re always in control.**  
    PlainNotes helps you understand your care without giving up your privacy.
    """)
