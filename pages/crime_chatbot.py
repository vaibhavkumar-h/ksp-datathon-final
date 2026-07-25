import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai

from auth import require_auth, render_logout_button
from styles import inject_custom_css


st.set_page_config(
    page_title="Crime AI Assistant",
    page_icon="🤖",
    layout="wide",
)
require_auth()
render_logout_button()
inject_custom_css()

# ---------------- LOAD ENV ---------------- #

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=API_KEY
)

# ---------------- LOAD DATA ---------------- #

df = pd.read_csv("data/district_wise_2023.csv")
df = df[df["Districts"] != "TOTAL"]

st.title("🤖 Karnataka Crime AI Assistant")

st.write(
    "Ask anything about Karnataka crime trends, districts, safety and recommendations."
)

st.divider()

# ---------------- QUICK QUESTIONS ---------------- #

c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("🔥 Highest Crime"):
        st.session_state.question = "Which district has highest crime?"

with c2:
    if st.button("🟢 Safest District"):
        st.session_state.question = "Which district is safest?"

with c3:
    if st.button("📈 Future Trends"):
        st.session_state.question = "Predict future crime trends."

with c4:
    if st.button("🚨 Recommendations"):
        st.session_state.question = "Give crime prevention recommendations."

question = st.text_input(
    "Ask AI...",
    value=st.session_state.get("question", "")
)

# ---------------- AI RESPONSE ---------------- #

if question:

    dataset_context = df.head(35).to_string()

    prompt = f"""
You are an AI Crime Analyst.

Dataset:

{dataset_context}

Answer this question:

{question}

Give detailed explanation and recommendations.
"""

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    st.write(response.text)

except Exception:
    st.warning(
        "Gemini quota exceeded. Showing local AI response."
    )

    if "safe" in question.lower():
        st.success(
            f"Safest district is "
            f"{df.sort_values('Total').iloc[0]['Districts']}"
        )

    elif "highest" in question.lower():
        st.error(
            f"Highest crime district is "
            f"{df.sort_values('Total',ascending=False).iloc[0]['Districts']}"
        )

    else:
        st.info(
            "AI service temporarily unavailable."
        )
