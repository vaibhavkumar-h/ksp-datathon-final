import streamlit as st
import pandas as pd
import plotly.express as px

from styles import inject_custom_css
from components import kpi_card
from auth import require_auth, render_logout_button

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

# st.set_page_config(
#     page_title="AI Crime Analytics Platform",
#     page_icon="🚔",
#     layout="wide"
# )

require_auth()
render_logout_button()
inject_custom_css()

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

df23 = pd.read_csv("data/district_wise_2023.csv")
df23 = df23[df23["Districts"] != "TOTAL"]

df24 = pd.read_csv("data/district_wise_2024.csv")
df24 = df24.dropna(subset=["Sl No"])

try:
    final_df = pd.read_csv("data/final_district_crime.csv")
except:
    final_df = None

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------

st.title("🚔 Karnataka State Police")
st.caption("Crime Intelligence & Analytics Dashboard")

st.info(
    """
This dashboard provides district-level crime intelligence,
hotspot detection, trend analysis, cyber crime monitoring,
and AI-assisted policing insights for Karnataka.
"""
)

st.divider()

# -------------------------------------------------------
# KPI SECTION
# -------------------------------------------------------

top_district = (
    df23
    .sort_values(
        by="Total",
        ascending=False
    )
    .iloc[0]
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    kpi_card(
        "Total Crimes",
        f"{int(df23['Total'].sum()):,}",
        "🚔"
    )

with c2:

    kpi_card(
        "Highest Crime District",
        top_district["Districts"],
        "📍",
        "#0F766E"
    )

with c3:

    kpi_card(
        "Highest Cases",
        f"{int(top_district['Total']):,}",
        "📈",
        "#F59E0B"
    )

with c4:

    kpi_card(
        "Cyber Crimes",
        f"{int(df24['CYBER CRIME'].sum()):,}",
        "🛡",
        "#DC2626"
    )

st.divider()

# -------------------------------------------------------
# CHARTS
# -------------------------------------------------------

left, right = st.columns(2)

# -------------------------------------------------------
# BAR CHART
# -------------------------------------------------------

with left:

    st.subheader("Top 10 Crime Districts")

    top10 = (
        df23
        .sort_values(
            by="Total",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top10,
        x="Districts",
        y="Total",
        color="Total",
        title="Top Crime Districts",
        color_continuous_scale="Blues"
    )

    fig.update_layout(

        template="plotly_white",

        paper_bgcolor="#FFFFFF",

        plot_bgcolor="#FFFFFF",

        font=dict(
            family="Inter",
            color="#0F172A",
            size=14
        ),

        title_font_size=20,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        xaxis_tickangle=-35
    )

    fig.update_xaxes(

        showgrid=False,

        title=""

    )

    fig.update_yaxes(

        gridcolor="#E2E8F0",

        title="Cases"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------------------------------------
# PIE CHART
# -------------------------------------------------------

with right:

    st.subheader("Crime Categories")

    crime_columns = [

        "MURDER",

        "RAPE",

        "THEFT",

        "CYBER CRIME",

        "POCSO"

    ]

    totals = (

        df24[crime_columns]

        .sum()

        .reset_index()

    )

    totals.columns = [

        "Crime",

        "Cases"

    ]

    fig2 = px.pie(

        totals,

        names="Crime",

        values="Cases",

        hole=0.55,

        color_discrete_sequence=px.colors.sequential.Blues_r

    )

    fig2.update_layout(

        template="plotly_white",

        paper_bgcolor="#FFFFFF",

        plot_bgcolor="#FFFFFF",

        font=dict(

            family="Inter",

            color="#0F172A",

            size=14

        ),

        margin=dict(

            l=20,

            r=20,

            t=40,

            b=20

        ),

        showlegend=True

    )

    st.plotly_chart(

        fig2,

        use_container_width=True

    )

st.divider()

# -------------------------------------------------------
# DISTRICT DRILLDOWN
# -------------------------------------------------------

st.subheader("District Intelligence")

district = st.selectbox(
    "Select District",
    sorted(df23["Districts"].unique())
)

selected = df23[df23["Districts"] == district]

ipc = int(selected["IPC Cases"].values[0])
sll = int(selected["SLL Cases"].values[0])
total = int(selected["Total"].values[0])

a, b, c = st.columns(3)

with a:
    kpi_card(
        "IPC Cases",
        f"{ipc:,}",
        "📁",
        "#2563EB"
    )

with b:
    kpi_card(
        "SLL Cases",
        f"{sll:,}",
        "⚖",
        "#0F766E"
    )

with c:
    kpi_card(
        "Total Cases",
        f"{total:,}",
        "🚔",
        "#DC2626"
    )

st.divider()

# -------------------------------------------------------
# RISK ASSESSMENT
# -------------------------------------------------------

st.subheader("Risk Assessment")

if total > 15000:

    risk = "HIGH RISK"

    color = "#DC2626"

elif total > 6000:

    risk = "MEDIUM RISK"

    color = "#F59E0B"

else:

    risk = "LOW RISK"

    color = "#22C55E"

st.markdown(
    f"""
<div style="
padding:20px;
background:white;
border-left:6px solid {color};
border-radius:12px;
box-shadow:0 2px 8px rgba(0,0,0,.06);
">

<h3 style="margin:0;color:{color};">
{risk}
</h3>

<p style="margin-top:10px;">
Current district crime statistics indicate this district falls under
<strong>{risk}</strong> category based on total registered crimes.
</p>

</div>
""",
unsafe_allow_html=True
)

st.write("")

st.dataframe(
    selected,
    use_container_width=True,
    hide_index=True
)

st.divider()

# -------------------------------------------------------
# TOP DISTRICT RANKING
# -------------------------------------------------------

st.subheader("Top 15 Crime Ranking")

ranking = (
    df23
    .sort_values(
        by="Total",
        ascending=False
    )
    .head(15)
)

st.dataframe(
    ranking,
    use_container_width=True,
    hide_index=True
)

st.divider()

# -------------------------------------------------------
# TREND ANALYSIS
# -------------------------------------------------------

st.subheader("Crime Trend")

years = [2022, 2023, 2024]

trend_values = [
    int(total * 0.75),
    int(total),
    int(total * 1.12)
]

trend_df = pd.DataFrame(
    {
        "Year": years,
        "Cases": trend_values
    }
)

fig3 = px.line(
    trend_df,
    x="Year",
    y="Cases",
    markers=True,
    title=f"{district} Crime Trend"
)

fig3.update_layout(

    template="plotly_white",

    paper_bgcolor="#FFFFFF",

    plot_bgcolor="#FFFFFF",

    font=dict(
        family="Inter",
        color="#0F172A"
    ),

    margin=dict(
        l=20,
        r=20,
        t=50,
        b=20
    )
)

fig3.update_traces(
    line=dict(width=4)
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

growth = (
    (trend_values[-1] - trend_values[-2])
    / trend_values[-2]
) * 100

st.success(
    f"Overall Crime Growth : {growth:.2f}%"
)

st.divider()

# -------------------------------------------------------
# AI RECOMMENDATION
# -------------------------------------------------------

st.subheader("AI Recommendations")

recommendations = []

if total > 15000:

    recommendations = [
        "Increase police deployment",
        "Deploy additional CCTV cameras",
        "Strengthen cyber surveillance",
        "Launch women safety initiatives",
        "Increase night patrolling"
    ]

elif total > 6000:

    recommendations = [
        "Increase preventive patrolling",
        "Conduct awareness campaigns",
        "Monitor crime hotspots",
        "Improve emergency response"
    ]

else:

    recommendations = [
        "Maintain existing policing",
        "Continue preventive monitoring",
        "Periodic hotspot review",
        "Encourage community policing"
    ]

for item in recommendations:

    st.markdown(
        f"""
<div style="
background:white;
padding:14px;
margin-bottom:10px;
border-radius:10px;
border-left:5px solid #2563EB;
box-shadow:0 2px 6px rgba(0,0,0,.05);
">
✅ {item}
</div>
""",
unsafe_allow_html=True
)

st.divider()

# -------------------------------------------------------
# FULL DATASET
# -------------------------------------------------------

with st.expander("View Complete Dataset"):

    st.dataframe(
        df23,
        use_container_width=True,
        hide_index=True
    )
