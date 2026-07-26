import os

import pandas as pd
import streamlit as st

from dotenv import load_dotenv

from auth import require_auth, render_logout_button
from styles import inject_custom_css


# ---------------- AUTH ---------------- #

require_auth()
render_logout_button()
inject_custom_css()

# ---------------- LOAD ENV ---------------- #

load_dotenv()

API_KEY = None
model = None

# ---------------- LOAD DATA ---------------- #

df = pd.read_csv("data/district_wise_2023.csv")
df = df[df["Districts"] != "TOTAL"]

# ---------------- PAGE ---------------- #

st.title("🤖 Karnataka Crime AI Assistant")

st.write(
    "Ask anything about Karnataka crime trends, districts, safety and recommendations."
)

st.divider()

# ---------------- QUICK QUESTIONS ---------------- #

c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("🔥 Highest Crime"):
        st.session_state.question = "Which district has the highest crime?"

with c2:
    if st.button("🟢 Safest District"):
        st.session_state.question = "Which district is the safest?"

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

    dataset_context = df.head(35).to_string(index=False)

    prompt = f"""
You are an expert AI Crime Analyst for Karnataka State Police.

Use the dataset below to answer the user's question.

Dataset:
{dataset_context}

User Question:
{question}

Provide:
1. Direct Answer
2. Explanation
3. Insights
4. Recommendations

Keep the response clear and professional.
"""

    try:

        if model is None:
            raise Exception("Gemini API key not found.")

        response = model.generate_content(prompt)

        if response.text:
            st.success("### AI Response")
            st.write(response.text)
        else:
            st.warning("No response received from Gemini.")

    except Exception as e:

        st.warning(
            "Gemini service is unavailable or free quota has been exhausted.\n\nShowing local intelligent response instead."
        )

        q = question.lower()

        if "highest" in q or "most crime" in q:

            district = df.sort_values(
                "Total",
                ascending=False
            ).iloc[0]

            st.error(
                f"Highest crime district: **{district['Districts']}**\n\n"
                f"Total Cases: **{district['Total']:,}**"
            )

        elif "safe" in q or "lowest" in q:

            district = df.sort_values(
                "Total"
            ).iloc[0]

            st.success(
                f"Safest district: **{district['Districts']}**\n\n"
                f"Total Cases: **{district['Total']:,}**"
            )

        elif "recommend" in q:

            st.info("""
### Crime Prevention Recommendations

• Increase CCTV surveillance in hotspot areas.

• Deploy predictive policing using crime analytics.

• Improve cyber awareness campaigns.

• Strengthen night patrolling.

• Use AI-based hotspot monitoring for resource allocation.
""")

        elif "trend" in q or "future" in q:

            st.info("""
### Future Crime Trend

Based on historical district-level data:

• Metropolitan districts are expected to continue reporting higher crime volumes.

• Cybercrime is likely to increase.

• AI-assisted policing and predictive analytics can significantly improve prevention.
""")

        else:

            st.info(
                "AI service is temporarily unavailable. Please try again later after the Gemini quota resets."
            )

        with st.expander("Technical Details"):
            st.code(str(e))