import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from styles import inject_custom_css
from auth import require_auth, render_logout_button

require_auth()
render_logout_button()
inject_custom_css()
st.title("📊 District Comparison Dashboard")

df = pd.read_csv("data/district_wise_2023.csv")
df = df[df["Districts"] != "TOTAL"]

district1 = st.selectbox(
    "Select District 1",
    df["Districts"],
    index=0
)

district2 = st.selectbox(
    "Select District 2",
    df["Districts"],
    index=1
)

row1 = df[df["Districts"] == district1].iloc[0]
row2 = df[df["Districts"] == district2].iloc[0]

comparison = pd.DataFrame({
    "Category": ["IPC Cases", "SLL Cases", "Total"],
    district1: [
        row1["IPC Cases"],
        row1["SLL Cases"],
        row1["Total"]
    ],
    district2: [
        row2["IPC Cases"],
        row2["SLL Cases"],
        row2["Total"]
    ]
})

st.dataframe(comparison)

fig, ax = plt.subplots(figsize=(8,5))

x = range(3)
width = 0.35

ax.bar(
    [i-width/2 for i in x],
    comparison[district1],
    width,
    label=district1
)

ax.bar(
    [i+width/2 for i in x],
    comparison[district2],
    width,
    label=district2
)

ax.set_xticks(x)
ax.set_xticklabels(comparison["Category"])
ax.set_ylabel("Cases")
ax.set_title("Crime Comparison")
ax.legend()

st.pyplot(fig)

if row1["Total"] > row2["Total"]:
    st.error(
        f"{district1} has higher crime than {district2}"
    )
else:
    st.success(
        f"{district2} has higher crime than {district1}"
    )
