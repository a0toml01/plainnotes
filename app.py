import streamlit as st
import openai
import os

# Set your OpenAI API key here or use environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="PlainNotes", page_icon="📝")

st.title("📝 PlainNotes")
st.subheader("Understand your doctor's notes – in plain language")

st.markdown("""
Welcome to **PlainNotes**, a tool that transforms complex clinical notes into easy-to-understand summaries.
Just paste your medical notes below, and we’ll simplify them into plain language.
""")

# User input for clinical notes
input_notes = st.text_area("Paste your doctor's notes here:", height=200)

# Summarize with OpenAI
if st.button("Summarize in Plain Language"):
    if not openai_api_key:
        st.error("OpenAI API key not found. Please set your API key in the environment variable 'OPENAI_API_KEY'.")
    elif not input_notes.strip():
        st.warning("Please paste some doctor's notes before submitting.")
    elif len(input_notes) > 3000:
        st.error("Note is too long. Please shorten the input to under 3000 characters.")
    else:
        openai.api_key = openai_api_key
        with st.spinner("Generating summary..."):
            try:
                prompt = (
                    "You are a medical communication assistant. Your job is to read the following doctor's note "
                    "and explain it in plain language at a 6th to 8th grade reading level. Use clear headers for each section: "
                    "'What this note says', 'Recommendations', and 'Medications/Conditions Explained'.\n\n"
                    f"Doctor's note:\n{input_notes}\n\nPlain language summary:"
                )

                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You simplify clinical notes into plain language summaries."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=600
                )

                summary = response.choices[0].message.content.strip()
                st.markdown("---")
                st.subheader("🧾 Summary")
                st.markdown(summary)
                st.success("Your summary has been generated.")

            except Exception as e:
                st.error(f"An error occurred while generating the summary: {e}")

st.caption("Note: This tool does not store or transmit any personal health information.")

with st.expander("🔐 Learn more about how we protect your privacy"):
    st.markdown("""
    **PlainNotes is privacy-first by design.**

    - We don’t require you to sign up or create an account.
    - Your notes are **not stored or logged** — once your summary is generated, the text is gone.
    - We use a secure AI model (like OpenAI’s GPT-4) to generate summaries, and that’s it.
    - You can remove names or personal details if you prefer — PlainNotes still works.

    **You’re always in control.**  
    PlainNotes helps you understand your care without giving up your privacy.
    """)
