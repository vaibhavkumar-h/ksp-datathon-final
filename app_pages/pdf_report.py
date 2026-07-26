import streamlit as st
import pandas as pd
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from styles import inject_custom_css
from auth import require_auth, render_logout_button

require_auth()
render_logout_button()
inject_custom_css()
st.title("📄 Crime Report Generator")

df = pd.read_csv("data/district_wise_2023.csv")

df = df[df["Districts"] != "TOTAL"]

district = st.selectbox(
    "Choose District",
    df["Districts"]
)

row = df[
    df["Districts"] == district
].iloc[0]

st.subheader("District Information")

st.write(f"IPC Cases : {row['IPC Cases']}")
st.write(f"SLL Cases : {row['SLL Cases']}")
st.write(f"Total Cases : {row['Total']}")

if st.button("Generate PDF"):

    filename = f"{district}_report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            f"<b>Crime Report - {district}</b>",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            f"IPC Cases : {row['IPC Cases']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"SLL Cases : {row['SLL Cases']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Total Cases : {row['Total']}",
            styles["Normal"]
        )
    )

    doc.build(elements)

    st.success("PDF Generated Successfully!")

    with open(filename, "rb") as file:

        st.download_button(
            label="⬇ Download PDF",
            data=file,
            file_name=filename,
            mime="application/pdf"
        )
