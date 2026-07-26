import streamlit as st
import pandas as pd
import numpy as np
from styles import inject_custom_css
from auth import require_auth, render_logout_button


# st.set_page_config(
#     page_title="Crime Alerts",
#     page_icon="🚨",
#     layout="wide"
# )
require_auth()
render_logout_button()
inject_custom_css()
# pulsing red-zone CSS for spike alerts
st.markdown("""
<style>
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(255,0,0,0.6); }
    70% { box-shadow: 0 0 0 15px rgba(255,0,0,0); }
    100% { box-shadow: 0 0 0 0 rgba(255,0,0,0); }
}
.pulse-alert {
    animation: pulse 1.5s infinite;
    background-color: #3b0d0d;
    border: 1px solid #ff4b4b;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
    color: #ffdddd;
}
</style>
""", unsafe_allow_html=True)

st.title("🚨 AI Crime Alerts System")


# ---------------------------------------------------------
# NORMALIZATION LAYER
# Each year's CSV uses a different schema. This function maps
# every year into a common shape: Districts | Total | Year
# ---------------------------------------------------------
def load_year(year):
    df = pd.read_csv(f"data/district_wise_{year}.csv")
    df.columns = df.columns.str.strip()

    # --- normalize the district-name column ---
    district_col_candidates = ["Districts", "DISTRICT/UNITS", "Districts/Units", "District"]
    district_col = next((c for c in district_col_candidates if c in df.columns), None)
    if district_col is None:
        st.error(f"⚠ {year} file has no recognizable district column. Found: {list(df.columns)}")
        st.stop()
    df = df.rename(columns={district_col: "Districts"})

    # --- normalize / derive the Total column ---
    if "Total" in df.columns:
        pass  # 2022, 2023 already have it
    elif "IPC/BNS Crimes" in df.columns and "SLL Crimes" in df.columns:
        df["Total"] = df["IPC/BNS Crimes"] + df["SLL Crimes"]  # 2025 shape
    else:
        # 2024 shape: sum every crime-category column
        exclude = ["Sl No", "Districts"]
        crime_cols = [c for c in df.columns if c not in exclude]
        df["Total"] = df[crime_cols].sum(axis=1, numeric_only=True)

    if "Sl No" in df.columns:
        df = df.dropna(subset=["Sl No"])

    df = df[df["Districts"].astype(str).str.strip().str.upper() != "TOTAL"]
    df["Year"] = year
    return df


df22 = load_year(2022)
df23 = load_year(2023)
df24 = load_year(2024)
df25 = load_year(2025)

st.divider()

st.subheader("🔥 High Risk District Alerts")

high = df23[df23["Total"] > 15000]

for _, row in high.iterrows():
    st.error(
        f"""
🚨 {row['Districts']}

Total Cases : {int(row['Total'])}

AI Recommendation:
Increase police patrolling and surveillance immediately.
"""
    )

st.divider()

st.subheader("🟠 Medium Risk Districts")

medium = df23[(df23["Total"] > 6000) & (df23["Total"] <= 15000)]

for _, row in medium.iterrows():
    st.warning(
        f"""
⚠ {row['Districts']}

Cases : {int(row['Total'])}

AI Recommendation:
Deploy preventive policing and awareness programs.
"""
    )

st.divider()

st.subheader("🟢 Safe Districts")

safe = df23[df23["Total"] <= 6000]

for _, row in safe.head(10).iterrows():
    st.success(
        f"""
✅ {row['Districts']}

Cases : {int(row['Total'])}

AI Recommendation:
Maintain current policing strategy.
"""
    )

st.divider()

# ---------------------------------------------------------
# Year-over-Year Trend Spike Alerts (district level)
# ---------------------------------------------------------
st.subheader("📈 Emerging Trend Alerts (Year-over-Year Spikes)")

combined = pd.concat(
    [df22[["Districts", "Total", "Year"]],
     df23[["Districts", "Total", "Year"]],
     df24[["Districts", "Total", "Year"]],
     df25[["Districts", "Total", "Year"]]],
    ignore_index=True
)

pivot = combined.pivot_table(
    index="Districts",
    columns="Year",
    values="Total",
    aggfunc="sum"
)

latest_year = pivot.columns.max()
history_years = [y for y in pivot.columns if y != latest_year]

pivot["Historical_Avg"] = pivot[history_years].mean(axis=1)
pivot["Latest"] = pivot[latest_year]
pivot["Pct_Change"] = (
    (pivot["Latest"] - pivot["Historical_Avg"]) / pivot["Historical_Avg"]
) * 100

spikes = pivot[pivot["Pct_Change"] > 25].sort_values("Pct_Change", ascending=False)

if spikes.empty:
    st.info("No major year-over-year spikes detected this cycle.")
else:
    for district, row in spikes.iterrows():
        st.markdown(
            f"""
<div class="pulse-alert">
🔴 <b>{district}</b> — {row['Pct_Change']:.1f}% increase vs historical average<br>
Historical Avg: {row['Historical_Avg']:.0f} cases &nbsp;|&nbsp; {latest_year}: {row['Latest']:.0f} cases<br>
<b>AI Recommendation:</b> Immediate resource reallocation and investigation review recommended.
</div>
""",
            unsafe_allow_html=True
        )

st.caption(
    "Note: district totals are normalized across years because raw category columns "
    "differ (e.g. 2024 reports individual offence types, 2025 reports IPC/SLL aggregates)."
)

st.divider()

# ---------------------------------------------------------
# Statistical Anomaly Detection (z-score based)
# ---------------------------------------------------------
st.subheader("🧠 AI Anomaly Detection")

pivot["Std_Dev"] = pivot[history_years].std(axis=1)
pivot["Z_Score"] = (pivot["Latest"] - pivot["Historical_Avg"]) / pivot["Std_Dev"].replace(0, np.nan)

anomalies = pivot[pivot["Z_Score"].abs() > 1.5].sort_values("Z_Score", ascending=False)

if anomalies.empty:
    st.info("No statistical anomalies detected in district-level crime totals.")
else:
    for district, row in anomalies.iterrows():
        direction = "above" if row["Z_Score"] > 0 else "below"
        st.warning(
            f"""
⚠ {district} — Anomaly Detected

This district's {latest_year} crime total is {abs(row['Z_Score']):.2f} standard deviations {direction} its historical pattern.

AI Recommendation:
Flag for manual review — deviation from expected behavioral pattern.
"""
        )

st.divider()

# ---------------------------------------------------------
# Crime Category Alerts (2024 only — the only file with
# category-level columns; 2022/2023/2025 only report
# IPC/SLL aggregates, so cross-year category comparison
# is not possible with the current dataset)
# ---------------------------------------------------------
st.subheader("🤖 Crime Category Alerts (2024 snapshot)")

exclude = ["Sl No", "Districts", "Total", "Year"]
crime_cols_2024 = [c for c in df24.columns if c not in exclude]

totals_24 = df24[crime_cols_2024].sum(numeric_only=True)

if not totals_24.empty:
    highest = totals_24.idxmax()
    cases = totals_24.max()

    st.error(
        f"""
🚨 Highest Volume Crime Category (2024)

Category : {highest}

Cases : {int(cases)}

AI Recommendation:
Special task force should focus on {highest}.
"""
    )

st.caption(
    "Category-level breakdown is only available in the 2024 dataset. "
    "2022/2023/2025 files report IPC/SLL aggregates only, so a multi-year "
    "category trend isn't possible without additional data."
)

st.divider()

st.subheader("📊 Alert Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("High Risk", len(high))
with c2:
    st.metric("Medium Risk", len(medium))
with c3:
    st.metric("Low Risk", len(safe))
with c4:
    st.metric("Anomalies", len(anomalies))
