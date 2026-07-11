"""
AI Learning Buddy — Streamlit App
Deliverable 7 for the AI Learning Buddy assignment (Pragati: Path to Future, Cohort 9)

SETUP:
1. pip install streamlit openai
2. Get an API key (OpenAI, or swap client below for Gemini/another provider)
3. Add your key as a Streamlit secret (see deployment steps at the bottom of this file)
4. Run locally with:  streamlit run app.py
"""

import streamlit as st
from openai import OpenAI

# ---------- CONFIG ----------
st.set_page_config(page_title="AI Learning Buddy", page_icon="🌱")

PERSONA_PROMPT = """You are Professor Byte, a calm and methodical AI tutor who specializes in
teaching programming and algorithm concepts to complete beginners. Rules you always follow:
(1) Explain new ideas using a simple, everyday analogy before using any technical term.
(2) Never use jargon without immediately defining it in plain language.
(3) Keep initial explanations under 150 words.
(4) When giving feedback, always be encouraging — name one thing the learner got right
    before addressing what to fix.
(5) Ask the learner a short check-in question after each explanation to keep them engaged.
(6) Stay strictly on the topic given to you; do not go off on tangents."""

TEMPLATES = {
    "Explain the topic": (
        "You are a patient tutor. Explain the concept of {topic} in simple, everyday "
        "language suitable for a complete beginner. Use exactly one relatable analogy. "
        "Keep the explanation under 150 words, and if you must use a technical term, "
        "define it in the same sentence."
    ),
    "Give a real-life example": (
        "Give me one clear, real-life example of {topic} in action that I would encounter "
        "in everyday life. Walk through it step by step, showing how each part of {topic} "
        "shows up in the example. Keep it under 100 words."
    ),
    "Generate a 5-question quiz": (
        "Generate 5 quiz questions about {topic} for a beginner learner. Use a mix of "
        "question types (multiple-choice, true/false, and short-answer). Number the "
        "questions. Do not reveal the answers yet — list them separately afterward under "
        "a heading called 'Answer Key', so the learner can attempt the quiz first."
    ),
    "Evaluate my answer": (
        "The topic is {topic}. The learner just answered a quiz question with: "
        "'{learner_answer}'. Tell the learner whether their answer is correct, partially "
        "correct, or incorrect. Point out one specific thing they got right. If they made "
        "a mistake, explain the misunderstanding gently and give one tip to improve."
    ),
    "Run a full session": (
        "You are an AI Learning Buddy for {topic}. Run the session in this order: "
        "(1) Explain {topic} simply. (2) Give one real-life example. "
        "(3) Ask if the learner is ready for a quiz. (4) Ask 5 quiz questions about "
        "{topic} one at a time. (5) After each answer, give brief, encouraging feedback. "
        "(6) At the end, summarize what the learner understood well and what to review."
    ),
}

# ---------- CLIENT ----------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def ask_buddy(user_prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": PERSONA_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content

# ---------- UI ----------
st.title("🧮 AI Learning Buddy")
st.caption("Meet Professor Byte — your patient coding & algorithms tutor.")

topic = st.text_input("What topic do you want to learn?", value="Binary Search")
activity = st.selectbox("What would you like to do?", list(TEMPLATES.keys()))

learner_answer = ""
if activity == "Evaluate my answer":
    learner_answer = st.text_area("Type your quiz answer here")

if st.button("Ask Professor Leaf"):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        prompt = TEMPLATES[activity].format(topic=topic, learner_answer=learner_answer)
        with st.spinner("Professor Byte is thinking..."):
            reply = ask_buddy(prompt)
        st.markdown("### Professor Byte says:")
        st.write(reply)

# ---------------------------------------------------------------------------
# DEPLOYMENT STEPS (Streamlit Community Cloud — free, ~5 minutes)
# ---------------------------------------------------------------------------
# 1. Create a free GitHub account (if you don't have one) and a new repository.
# 2. Add two files to that repo:
#       - app.py            (this file)
#       - requirements.txt  (containing: streamlit\nopenai)
# 3. Go to https://share.streamlit.io and sign in with GitHub.
# 4. Click "New app", select your repo, branch, and app.py as the entry point.
# 5. Before deploying, click "Advanced settings" -> "Secrets" and add:
#       OPENAI_API_KEY = "sk-...your-key..."
# 6. Click "Deploy". After a minute you'll get a public URL like:
#       https://your-app-name.streamlit.app
# 7. Open that link in a fresh browser tab to confirm it works, then paste it
#    into Section 7 of AI_Learning_Buddy_Submission.docx.
# ---------------------------------------------------------------------------
