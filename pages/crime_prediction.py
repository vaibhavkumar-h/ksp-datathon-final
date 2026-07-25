import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
from styles import inject_custom_css
from auth import require_auth, render_logout_button

st.set_page_config(
    page_title="Crime Prediction",
    layout="wide"
)
require_auth()
render_logout_button()
inject_custom_css()

st.title("🤖 AI Crime Prediction & Risk Scoring")

st.caption(
    "Machine Learning based crime forecasting using Karnataka crime datasets (2022-2025)"
)

# ===========================
# LOAD DATA
# ===========================

df22 = pd.read_csv("data/district_wise_2022.csv")
df23 = pd.read_csv("data/district_wise_2023.csv")
df25 = pd.read_csv("data/district_wise_2025.csv")

# remove total rows
df22 = df22[df22["Districts"] != "TOTAL"]
df23 = df23[df23["Districts"] != "TOTAL"]
df25 = df25[df25["Districts/Units"] != "TOTAL"]

districts = sorted(df23["Districts"].unique())

district = st.selectbox(
    "Choose District",
    districts
)

# ===========================
# GET DISTRICT DATA
# ===========================

c22 = df22.loc[
    df22["Districts"] == district,
    "Total"
].values[0]

c23 = df23.loc[
    df23["Districts"] == district,
    "Total"
].values[0]

# 2025 file has IPC + SLL
row25 = df25[
    df25["Districts/Units"] == district
]

if len(row25) > 0:

    c25 = (
        row25["IPC/BNS Crimes"].values[0]
        + row25["SLL Crimes"].values[0]
    )

else:
    c25 = c23

# approximate 2024 value
c24 = int((c23 + c25) / 2)

# ===========================
# MACHINE LEARNING MODEL
# ===========================

X = np.array([2022, 2023, 2024, 2025]).reshape(-1, 1)

y = np.array([
    c22,
    c23,
    c24,
    c25
])

model = LinearRegression()

model.fit(X, y)

pred26 = int(
    model.predict([[2026]])[0]
)

pred27 = int(
    model.predict([[2027]])[0]
)

# ===========================
# METRICS
# ===========================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Predicted 2026",
        f"{pred26:,}"
    )

with col2:
    st.metric(
        "Predicted 2027",
        f"{pred27:,}"
    )

growth = (
    (pred27 - c25)
    / c25
) * 100

with col3:
    st.metric(
        "Growth %",
        f"{growth:.2f}%"
    )

# ===========================
# RISK CLASSIFICATION
# ===========================

st.markdown("---")

st.subheader("🚨 Risk Assessment")

if pred27 > 50000:

    st.error(
        "🔴 HIGH RISK DISTRICT"
    )

elif pred27 > 10000:

    st.warning(
        "🟠 MEDIUM RISK DISTRICT"
    )

else:

    st.success(
        "🟢 LOW RISK DISTRICT"
    )

# ===========================
# FORECAST GRAPH
# ===========================

years = [
    2022,
    2023,
    2024,
    2025,
    2026,
    2027
]

cases = [
    c22,
    c23,
    c24,
    c25,
    pred26,
    pred27
]

fig, ax = plt.subplots(
    figsize=(12, 6)
)

ax.plot(
    years,
    cases,
    marker="o",
    linewidth=3
)

ax.set_title(
    f"Crime Forecast : {district}",
    fontsize=20
)

ax.set_xlabel("Year")
ax.set_ylabel("Cases")

ax.grid(True)

st.pyplot(fig)

# ===========================
# HISTORICAL TABLE
# ===========================

st.subheader(
    "📊 Historical Crime Data"
)

history = pd.DataFrame({

    "Year": years,

    "Cases": cases

})

st.dataframe(
    history,
    use_container_width=True
)

# ===========================
# AI RECOMMENDATIONS
# ===========================

st.subheader(
    "🧠 AI Recommendations"
)

if pred27 > 50000:

    st.write("""
    • Increase police patrolling

    • Deploy AI CCTV surveillance

    • Strengthen cyber crime units

    • Create rapid response teams

    • Increase night patrol vehicles
    """)

elif pred27 > 10000:

    st.write("""
    • Increase public awareness

    • Monitor emerging hotspots

    • Improve community policing

    • Strengthen women safety initiatives
    """)

else:

    st.write("""
    • Maintain current policing

    • Continue preventive monitoring

    • Focus on early detection systems
    """)
