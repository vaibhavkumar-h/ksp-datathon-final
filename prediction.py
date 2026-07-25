import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(
    page_title="Crime Prediction",
    layout="wide"
)

st.title("🤖 AI Crime Prediction & Risk Scoring")

# =====================
# LOAD DATA
# =====================

df22 = pd.read_csv("data/district_wise_2022.csv")
df23 = pd.read_csv("data/district_wise_2023.csv")
df25 = pd.read_csv("data/district_wise_2025.csv")

df22 = df22[df22["Districts"] != "TOTAL"]
df23 = df23[df23["Districts"] != "TOTAL"]

# 2025 column names differ
df25 = df25[df25["Districts/Units"] != "Commissionerates"]

district = st.selectbox(
    "Choose District",
    sorted(df22["Districts"])
)

# =====================
# GET VALUES
# =====================

c22 = int(
    df22[df22["Districts"] == district]["Total"].iloc[0]
)

c23 = int(
    df23[df23["Districts"] == district]["Total"].iloc[0]
)

# Try matching district names in 2025 file

try:

    c25 = int(
        (
            df25[
                df25["Districts/Units"]
                == district
            ]["IPC/BNS Crimes"]
            +
            df25[
                df25["Districts/Units"]
                == district
            ]["SLL Crimes"]
        ).iloc[0]
    )

except:

    c25 = c23

# Approximate 2024
c24 = int((c23 + c25) / 2)

# =====================
# TRAIN MODEL
# =====================

X = np.array(
    [2022,2023,2024,2025]
).reshape(-1,1)

y = np.array(
    [c22,c23,c24,c25]
)

model = LinearRegression()

model.fit(X,y)

pred26 = int(
    model.predict([[2026]])[0]
)

pred27 = int(
    model.predict([[2027]])[0]
)

# =====================
# KPI
# =====================

c1,c2 = st.columns(2)

c1.metric(
    "Predicted 2026",
    pred26
)

c2.metric(
    "Predicted 2027",
    pred27
)

# =====================
# GRAPH
# =====================

years = [
    2022,
    2023,
    2024,
    2025,
    2026,
    2027
]

values = [
    c22,
    c23,
    c24,
    c25,
    pred26,
    pred27
]

fig, ax = plt.subplots(
    figsize=(12,5)
)

ax.plot(
    years,
    values,
    marker="o",
    linewidth=3
)

ax.set_title(
    f"Crime Forecast : {district}"
)

ax.set_ylabel(
    "Cases"
)

ax.grid(True)

st.pyplot(fig)

# =====================
# RISK SCORE
# =====================

st.markdown("---")

if pred27 > 20000:

    st.error(
        f"🔴 HIGH RISK DISTRICT : {district}"
    )

elif pred27 > 7000:

    st.warning(
        f"🟠 MEDIUM RISK DISTRICT : {district}"
    )

else:

    st.success(
        f"🟢 LOW RISK DISTRICT : {district}"
    )

# =====================
# TREND ALERT
# =====================

change = (
    (pred27 - c25)
    / c25
) * 100

st.subheader("🚨 Trend Alert")

if change > 15:

    st.error(
        f"Crime may increase by {change:.1f}%"
    )

elif change > 0:

    st.warning(
        f"Crime may increase by {change:.1f}%"
    )

else:

    st.success(
        f"Crime may decrease by {abs(change):.1f}%"
    )