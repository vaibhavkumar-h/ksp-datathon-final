import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from styles import inject_custom_css
from auth import require_auth, render_logout_button


# ==========================
# PAGE SETTINGS
# ==========================

st.set_page_config(
    page_title="Crime Hotspots",
    page_icon="🗺️",
    layout="wide"
)
require_auth()
render_logout_button()
inject_custom_css()
st.title("🗺️ Karnataka Crime Hotspot Detection")
st.markdown("Interactive AI-based crime hotspot visualization")

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv("data/district_wise_2023.csv")

df = df[df["Districts"] != "TOTAL"]

df["Total"] = pd.to_numeric(df["Total"])

# ==========================
# DISTRICT COORDINATES
# ==========================

coords = {

    "Bagalkot":[16.18,75.69],
    "Bengaluru City":[12.97,77.59],
    "Bengaluru District":[13.10,77.60],
    "Belagavi District":[15.85,74.50],
    "Ballari":[15.14,76.92],
    "Bidar":[17.91,77.52],
    "Vijayapura":[16.83,75.71],
    "Chikkaballapura":[13.43,77.73],
    "Chamarajnagar":[11.92,76.95],
    "Chikkamagaluru":[13.31,75.77],
    "Chitradurga":[14.23,76.40],
    "Dakshina Kannada":[12.87,74.88],
    "Davanagere":[14.46,75.92],
    "Dharwad":[15.45,75.00],
    "Gadag":[15.43,75.63],
    "Kalaburgi":[17.33,76.83],
    "Hassan":[13.00,76.10],
    "Haveri":[14.80,75.40],
    "Hubballi Dharwad City":[15.36,75.12],
    "Kodagu":[12.42,75.73],
    "Kolar":[13.14,78.13],
    "Koppal":[15.34,76.15],
    "Mandya":[12.52,76.90],
    "Mangaluru City":[12.91,74.85],
    "Mysuru City":[12.30,76.64],
    "Mysuru District":[12.29,76.64],
    "Raichur":[16.21,77.35],
    "Ramanagara":[12.72,77.28],
    "Shimoga":[13.93,75.57],
    "Tumakuru":[13.34,77.10],
    "Udupi":[13.34,74.74],
    "Uttara Kannada":[14.80,74.13],
    "Yadgiri":[16.77,77.13],
    "Belagavi City":[15.85,74.50],
    "Kalaburgi City":[17.33,76.83],
    "Vijayanagara":[15.33,76.46],
    "KGF":[12.95,78.27]
}

# ==========================
# CREATE MAP
# ==========================

m = folium.Map(
    location=[15.1,76.0],
    zoom_start=7.5,
    tiles="CartoDB dark_matter"
)

m.fit_bounds([
    [11.5,74],
    [18,78]
])

# ==========================
# ADD HOTSPOTS
# ==========================

for _, row in df.iterrows():

    district = row["Districts"]

    if district in coords:

        crimes = row["Total"]

        lat, lon = coords[district]

        radius = max(5, (crimes ** 0.5)/8)

        # Risk Classification

        if crimes > 15000:
            color = "red"
            risk = "HIGH 🔴"

        elif crimes > 6000:
            color = "orange"
            risk = "MEDIUM 🟠"

        else:
            color = "green"
            risk = "LOW 🟢"

        folium.CircleMarker(

            location=[lat, lon],

            radius=radius,

            tooltip=f"{district}",

            popup=f"""
            <h3>{district}</h3>

            Total Crimes : {int(crimes)}

            <br><br>

            Risk Level : {risk}
            """,

            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.75

        ).add_to(m)

# ==========================
# SHOW MAP
# ==========================

st_folium(
    m,
    width=1500,
    height=700
)

# ==========================
# LEGEND
# ==========================

st.markdown("---")

st.subheader("🚨 Risk Classification")

c1, c2, c3 = st.columns(3)

with c1:
    st.success("🟢 LOW RISK\n\nCrime < 6000")

with c2:
    st.warning("🟠 MEDIUM RISK\n\n6000 - 15000")

with c3:
    st.error("🔴 HIGH RISK\n\nCrime > 15000")

# ==========================
# TOP DISTRICTS TABLE
# ==========================

st.markdown("---")

st.subheader("🏆 Top 10 Crime Districts")

top = df.sort_values(
    by="Total",
    ascending=False
).head(10)

st.dataframe(
    top,
    use_container_width=True
)

# ==========================
# DISTRICT SEARCH
# ==========================

st.markdown("---")

st.subheader("🔍 District Drilldown")

selected = st.selectbox(
    "Choose District",
    sorted(df["Districts"])
)

temp = df[df["Districts"] == selected]

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "IPC Cases",
        int(temp["IPC Cases"].iloc[0])
    )

with c2:
    st.metric(
        "SLL Cases",
        int(temp["SLL Cases"].iloc[0])
    )

with c3:
    st.metric(
        "Total Cases",
        int(temp["Total"].iloc[0])
    )

st.dataframe(
    temp,
    use_container_width=True
)
