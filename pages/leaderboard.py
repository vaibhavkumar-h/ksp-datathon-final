import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from styles import inject_custom_css
from auth import require_auth, render_logout_button


st.set_page_config(
    page_title="Crime Leaderboard",
    page_icon="🏆",
    layout="wide"
)
require_auth()
render_logout_button()
inject_custom_css()
# ---------------- LOAD DATA ---------------- #

df = pd.read_csv("data/district_wise_2023.csv")
df = df[df["Districts"] != "TOTAL"]

df["Total"] = pd.to_numeric(df["Total"], errors="coerce")
df = df.dropna(subset=["Total"])

# ---------------- TITLE ---------------- #

st.title("🏆 Karnataka Crime Leaderboard")
st.markdown(
    "District rankings based on total crime statistics."
)

st.divider()

# ---------------- TOP 10 DANGEROUS ---------------- #

top10 = (
    df.sort_values(
        by="Total",
        ascending=False
    )
    .head(10)
)

st.subheader("🚨 Top Dangerous Districts")

danger_df = top10[
    ["Districts", "IPC Cases", "SLL Cases", "Total"]
].reset_index(drop=True)

danger_df.index += 1

st.dataframe(
    danger_df,
    use_container_width=True
)

# ---------------- SAFEST ---------------- #

st.subheader("🟢 Safest Districts")

safe_df = (
    df.sort_values(
        by="Total",
        ascending=True
    )
    .head(10)
)

safe_df = safe_df[
    ["Districts", "IPC Cases", "SLL Cases", "Total"]
].reset_index(drop=True)

safe_df.index += 1

st.dataframe(
    safe_df,
    use_container_width=True
)

st.divider()

# ---------------- BAR GRAPH ---------------- #

left, right = st.columns(2)

with left:

    st.subheader("📊 Most Dangerous Districts")

    fig1, ax1 = plt.subplots(figsize=(8,5))

    ax1.bar(
        top10["Districts"],
        top10["Total"]
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.ylabel("Cases")

    st.pyplot(fig1)

with right:

    st.subheader("🟢 Safest Districts")

    fig2, ax2 = plt.subplots(figsize=(8,5))

    ax2.bar(
        safe_df["Districts"],
        safe_df["Total"]
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.ylabel("Cases")

    st.pyplot(fig2)

st.divider()

# ---------------- RISK LEVEL ---------------- #

st.subheader("🚨 Risk Classification")

ranking = df.copy()

risk = []

for value in ranking["Total"]:

    if value > 15000:
        risk.append("🔴 HIGH")

    elif value > 6000:
        risk.append("🟠 MEDIUM")

    else:
        risk.append("🟢 LOW")

ranking["Risk"] = risk

ranking = ranking.sort_values(
    by="Total",
    ascending=False
)

ranking = ranking[
    ["Districts", "Total", "Risk"]
]

ranking.reset_index(drop=True, inplace=True)

ranking.index += 1

st.dataframe(
    ranking,
    use_container_width=True
)

st.divider()

# ---------------- AI INSIGHTS ---------------- #

st.subheader("🤖 AI Insights")

highest = top10.iloc[0]
lowest = safe_df.iloc[0]

st.success(
    f"""
🚨 Highest Crime District: {highest['Districts']}
with {int(highest['Total']):,} cases.

🟢 Safest District: {lowest['Districts']}
with {int(lowest['Total']):,} cases.

⚠ Bengaluru region dominates overall crime statistics.
"""
)
