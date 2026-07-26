import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

from styles import inject_custom_css
from auth import require_auth, render_logout_button

# st.set_page_config(
#     page_title="Crime Hotspot Map",
#     page_icon="🗺️",
#     layout="wide"
# )

require_auth()
render_logout_button()
inject_custom_css()

st.title("🗺️ Spatiotemporal Crime Hotspot Map")
st.caption(
    "Built from real FIR-level records (geocoded lat/long, year/month/day). "
    "Filter below to see where and when crime clusters in Karnataka. "
    "Note: this dataset has day-of-month granularity, not hour-of-day — "
    "so this shows seasonal/monthly hotspot shifts, not time-of-day patterns."
)


@st.cache_data
def load_fir_data():
    # KGID column had a mixed-dtype warning on load — force it to string
    df = pd.read_csv(
        "data/fir_karnataka.csv",
        dtype={"KGID": str},
        low_memory=False
    )

    df = df.dropna(subset=["Latitude", "Longitude"])

    # sanity filter: Karnataka's real lat/long bounds, drops bad geocodes
    df = df[
        df["Latitude"].between(11, 19) &
        df["Longitude"].between(74, 79)
    ]

    return df


df = load_fir_data()

st.divider()

# ---------------------------------------------------------
# FILTERS
# ---------------------------------------------------------
f1, f2, f3, f4 = st.columns(4)

with f1:
    years = sorted(df["FIR_YEAR"].dropna().unique())
    selected_year = st.selectbox("Year", years, index=len(years) - 1)

with f2:
    months_available = sorted(
        df[df["FIR_YEAR"] == selected_year]["FIR_MONTH"].dropna().unique()
    )
    selected_month = st.selectbox("Month", ["All"] + [int(m) for m in months_available])

with f3:
    districts = sorted(df["District_Name"].dropna().unique())
    selected_district = st.selectbox("District", ["All"] + list(districts))

with f4:
    crime_types = sorted(df["CrimeHead_Name"].dropna().unique())
    selected_crime = st.selectbox("Crime Type", ["All"] + list(crime_types))

filtered = df[df["FIR_YEAR"] == selected_year]

if selected_month != "All":
    filtered = filtered[filtered["FIR_MONTH"] == selected_month]

if selected_district != "All":
    filtered = filtered[filtered["District_Name"] == selected_district]

if selected_crime != "All":
    filtered = filtered[filtered["CrimeHead_Name"] == selected_crime]

st.divider()

st.metric("Incidents in this selection", f"{len(filtered):,}")

# ---------------------------------------------------------
# HEATMAP
# ---------------------------------------------------------
if filtered.empty:
    st.warning("No incidents match this filter combination.")
else:
    center_lat = filtered["Latitude"].mean()
    center_lon = filtered["Longitude"].mean()

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=7,
        tiles="CartoDB dark_matter"
    )

    heat_points = filtered[["Latitude", "Longitude"]].values.tolist()

    # cap points for render performance — density is what matters, not every dot
    MAX_POINTS = 20000
    if len(heat_points) > MAX_POINTS:
        heat_points = (
            filtered.sample(MAX_POINTS, random_state=42)[["Latitude", "Longitude"]]
            .values.tolist()
        )
        st.caption(f"Showing a random sample of {MAX_POINTS:,} of {len(filtered):,} incidents for map performance.")

    HeatMap(heat_points, radius=8, blur=12).add_to(m)

    st_folium(m, width=1400, height=550)

st.divider()

# ---------------------------------------------------------
# MONTHLY TREND (within selected year)
# ---------------------------------------------------------
st.subheader("📈 Monthly Trend (selected year)")

year_df = df[df["FIR_YEAR"] == selected_year]
if selected_district != "All":
    year_df = year_df[year_df["District_Name"] == selected_district]
if selected_crime != "All":
    year_df = year_df[year_df["CrimeHead_Name"] == selected_crime]

monthly_counts = (
    year_df.groupby("FIR_MONTH")
    .size()
    .reindex(range(1, 13), fill_value=0)
)

st.bar_chart(monthly_counts)

avg_monthly = monthly_counts.mean()
peak_month = monthly_counts.idxmax()
peak_value = monthly_counts.max()

if peak_value > avg_monthly * 1.25:
    st.info(
        f"🤖 **AI Insight:** Month {peak_month} shows {peak_value:,} incidents, "
        f"{((peak_value / avg_monthly) - 1) * 100:.0f}% above this year's monthly average "
        f"({avg_monthly:.0f}). This may indicate a seasonal spike worth investigating."
    )

st.divider()

# ---------------------------------------------------------
# TOP CRIME TYPES IN SELECTION
# ---------------------------------------------------------
st.subheader("🔍 Top Crime Types in Selection")

if not filtered.empty:
    top_crimes = (
        filtered["CrimeHead_Name"]
        .value_counts()
        .head(10)
        .reset_index()
    )
    top_crimes.columns = ["Crime Type", "Incidents"]
    st.dataframe(top_crimes, use_container_width=True, hide_index=True)