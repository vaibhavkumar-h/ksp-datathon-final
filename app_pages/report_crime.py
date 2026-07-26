import streamlit as st
import pandas as pd
import os
import uuid
from datetime import datetime

from styles import inject_custom_css
from auth import require_auth, render_logout_button

# st.set_page_config(
#     page_title="Report a Crime",
#     page_icon="📢",
#     layout="wide"
# )

require_auth()
render_logout_button()
inject_custom_css()

st.title("📢 Report a Crime")
st.caption(
    "Citizen/officer-submitted incident reporting. Unlike the historical district-wise "
    "datasets, every submission here captures an exact date AND time — over time this "
    "builds the timestamped data needed for true time-of-day hotspot analysis."
)

st.divider()

REPORTS_FILE = "data/citizen_reports.csv"

URGENT_KEYWORDS = [
    "murder", "rape", "kidnap", "weapon", "gun", "knife", "acid",
    "assault", "bomb", "explosive", "hostage", "trafficking"
]


def classify_urgency(text):
    t = text.lower()
    for kw in URGENT_KEYWORDS:
        if kw in t:
            return "HIGH"
    return "NORMAL"


DISTRICTS = [
    "Bengaluru City", "Bengaluru District", "Mysuru City", "Mysuru District",
    "Belagavi City", "Belagavi District", "Kalaburagi", "Ballari", "Vijayapura",
    "Tumakuru", "Shimoga", "Hassan", "Mandya", "Chitradurga", "Chikkamagaluru",
    "Chamarajanagar", "Kodagu", "Dakshina Kannada", "Udupi", "Uttara Kannada",
    "Dharwad", "Gadag", "Haveri", "Koppal", "Raichur", "Bidar", "Bagalkot",
    "Chikkaballapura", "Kolar", "Ramanagara", "Yadgir", "Davanagere"
]

CRIME_TYPES = [
    "Theft", "Burglary", "Robbery", "Assault", "Murder", "Cyber Crime",
    "Domestic Violence", "Women Safety", "Molestation", "Traffic Accident",
    "Drug-related", "Fraud/Cheating", "Public Nuisance", "Other"
]

with st.form("crime_report_form", clear_on_submit=True):

    anonymous = st.checkbox("Submit anonymously")

    c1, c2 = st.columns(2)
    with c1:
        reporter_name = st.text_input("Your Name (leave blank if anonymous)")
    with c2:
        contact_number = st.text_input("Contact Number (optional)")

    c3, c4 = st.columns(2)
    with c3:
        district = st.selectbox("District", DISTRICTS)
    with c4:
        area = st.text_input("Area / Locality")

    c5, c6, c7 = st.columns(3)
    with c5:
        crime_type = st.selectbox("Crime Type", CRIME_TYPES)
    with c6:
        incident_date = st.date_input("Date of Incident")
    with c7:
        incident_time = st.time_input("Time of Incident")

    description = st.text_area("Describe what happened", height=140)

    submitted = st.form_submit_button("Submit Report")

    if submitted:
        if not description.strip():
            st.error("Please describe the incident before submitting.")
        else:
            complaint_id = "CR-" + uuid.uuid4().hex[:8].upper()
            urgency = classify_urgency(description + " " + crime_type)

            new_row = pd.DataFrame([{
                "Complaint_ID": complaint_id,
                "Timestamp": datetime.now().isoformat(timespec="seconds"),
                "Reporter": "Anonymous" if anonymous else (reporter_name.strip() or "Anonymous"),
                "Contact": "" if anonymous else contact_number.strip(),
                "District": district,
                "Area": area.strip(),
                "Crime_Type": crime_type,
                "Incident_Date": str(incident_date),
                "Incident_Time": str(incident_time),
                "Description": description.strip(),
                "Urgency": urgency
            }])

            file_exists = os.path.exists(REPORTS_FILE)
            new_row.to_csv(
                REPORTS_FILE,
                mode="a" if file_exists else "w",
                header=not file_exists,
                index=False
            )

            if urgency == "HIGH":
                st.error(
                    f"🚨 Report submitted — Complaint ID **{complaint_id}**\n\n"
                    f"This report has been flagged **HIGH PRIORITY** based on the description "
                    f"and routed for immediate review."
                )
            else:
                st.success(
                    f"✅ Report submitted — Complaint ID **{complaint_id}**\n\n"
                    f"Thank you, your report has been logged for review."
                )

st.divider()

st.subheader("📋 Recent Reports (demo view)")

if os.path.exists(REPORTS_FILE):
    reports_df = pd.read_csv(REPORTS_FILE)

    m1, m2 = st.columns(2)
    with m1:
        st.metric("Total Reports Logged", len(reports_df))
    with m2:
        st.metric("High Priority Reports", int((reports_df["Urgency"] == "HIGH").sum()))

    st.dataframe(
        reports_df.sort_values("Timestamp", ascending=False).head(10),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No reports submitted yet.")