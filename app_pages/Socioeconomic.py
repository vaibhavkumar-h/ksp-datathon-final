import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from styles import inject_custom_css
from auth import require_auth, render_logout_button


# st.set_page_config(
#     page_title="Socio-Economic Correlation",
#     page_icon="🏙️",
#     layout="wide"
# )
require_auth()
render_logout_button()
inject_custom_css()
st.title("🏙️ Socio-Economic Correlation Dashboard")
st.caption(
    "Overlays 2011 Census population & urbanization data with recent crime totals "
    "to explore the relationship between urbanization and crime volume."
)

st.divider()

# ---------------------------------------------------------
# STEP 1: Load population data (2011 Census, all-India file
# filtered to Karnataka) and load latest crime totals
# ---------------------------------------------------------
pop_df = pd.read_csv("data/karnataka_population.csv")
pop_df.columns = pop_df.columns.str.strip()
pop_df = pop_df[pop_df["State name"].str.upper() == "KARNATAKA"].copy()

# crime data — using 2023 file since it has a clean Total column
# (2024/2025 have different schemas, see alerts.py normalization)
crime_df = pd.read_csv("data/district_wise_2023.csv")
crime_df.columns = crime_df.columns.str.strip()
crime_df = crime_df[crime_df["Districts"].str.upper() != "TOTAL"].copy()


# ---------------------------------------------------------
# STEP 2: Name-mapping layer
# Karnataka renamed several districts in 2014. The 2011 census
# file uses the OLD names; crime data may use OLD or NEW names
# depending on the file. This map normalizes both sides.
# ---------------------------------------------------------
RENAME_MAP = {
    "BANGALORE": "BENGALURU",
    "BANGALORE URBAN": "BENGALURU URBAN",
    "BANGALORE RURAL": "BENGALURU RURAL",
    "BELGAUM": "BELAGAVI",
    "BELLARY": "BALLARI",
    "BIJAPUR": "VIJAYAPURA",
    "CHAMARAJANAGAR": "CHAMARAJANAGARA",
    "CHIKMAGALUR": "CHIKKAMAGALURU",
    "GULBARGA": "KALABURAGI",
    "MYSORE": "MYSURU",
    "SHIMOGA": "SHIVAMOGGA",
    "TUMKUR": "TUMAKURU",
}


def normalize_name(name):
    n = str(name).strip().upper()
    n = " ".join(n.split())  # collapse repeated whitespace

    # Bengaluru is the ONLY district split into Urban/Rural — these are
    # genuinely different districts, so they need explicit handling
    # instead of generic suffix stripping (which was colliding them).
    bengaluru_overrides = {
        "BANGALORE": "BENGALURU URBAN",
        "BANGALORE URBAN": "BENGALURU URBAN",
        "BANGALORE RURAL": "BENGALURU RURAL",
        "BENGALURU": "BENGALURU URBAN",
        "BENGALURU CITY": "BENGALURU URBAN",
        "BENGALURU URBAN": "BENGALURU URBAN",
        "BENGALURU DISTRICT": "BENGALURU RURAL",
        "BENGALURU RURAL": "BENGALURU RURAL",
    }
    if n in bengaluru_overrides:
        return bengaluru_overrides[n]

    # For every other district, "District"/"City" suffixes don't carry
    # distinguishing meaning, so it's safe to strip them here.
    for suffix in [" DISTRICT", " CITY"]:
        if n.endswith(suffix):
            n = n[: -len(suffix)]
    n = n.strip()

    return RENAME_MAP.get(n, n)


pop_df["match_key"] = pop_df["District name"].apply(normalize_name)
crime_df["match_key"] = crime_df["Districts"].apply(normalize_name)

merged = pd.merge(
    crime_df[["Districts", "Total", "match_key"]],
    pop_df[["District name", "Population", "Rural_Households", "Urban_Households", "match_key"]],
    on="match_key",
    how="inner"
)

unmatched_crime = crime_df[~crime_df["match_key"].isin(merged["match_key"])]
unmatched_pop = pop_df[~pop_df["match_key"].isin(merged["match_key"])]

# Population starts as int64 (whole census counts), but the jurisdiction-split
# logic below assigns fractional estimates into it — cast to float first so
# pandas doesn't reject the assignment.
merged["Population"] = merged["Population"].astype(float)


# ---------------------------------------------------------
# STEP 2b: Handle City/District jurisdiction splits
# Some districts (e.g. Belagavi, Mysuru) appear as TWO rows in
# crime data ("X City" and "X District") but only ONE row in the
# census population data — because the census tracks the whole
# administrative district, not the police-jurisdiction split.
# Assigning the full district population to both rows would
# double-count it. Instead, split the district's population using
# its own urban/rural household ratio: the "City" row gets the
# urban-estimated share, the "District" row gets the rural share.
# ---------------------------------------------------------
def classify_jurisdiction(original_name):
    u = str(original_name).upper()
    if "CITY" in u:
        return "URBAN"
    if "DISTRICT" in u or "RURAL" in u:
        return "RURAL"
    return None


dupe_keys = merged["match_key"].value_counts()
dupe_keys = dupe_keys[dupe_keys > 1].index

split_rows = []
for key in dupe_keys:
    group = merged[merged["match_key"] == key].copy()
    total_hh = group["Urban_Households"].iloc[0] + group["Rural_Households"].iloc[0]
    urban_frac = group["Urban_Households"].iloc[0] / total_hh
    rural_frac = 1 - urban_frac

    for idx, row in group.iterrows():
        jurisdiction = classify_jurisdiction(row["Districts"])
        if jurisdiction == "URBAN":
            merged.loc[idx, "Population"] = row["Population"] * urban_frac
            merged.loc[idx, "Urbanization_Pct_Override"] = 100.0
        elif jurisdiction == "RURAL":
            merged.loc[idx, "Population"] = row["Population"] * rural_frac
            merged.loc[idx, "Urbanization_Pct_Override"] = 0.0
        else:
            # can't tell which is which — split evenly and flag it
            merged.loc[idx, "Population"] = row["Population"] / len(group)
            merged.loc[idx, "Urbanization_Pct_Override"] = np.nan

if not dupe_keys.empty:
    st.warning(
        f"⚠ These districts are split into City/District jurisdictions in your crime "
        f"data but share one census population figure — population was estimated "
        f"proportionally using household ratios: {list(dupe_keys)}"
    )

# ---------------------------------------------------------
# STEP 3: Derived metrics
# ---------------------------------------------------------
merged["Urbanization_Pct"] = (
    merged["Urban_Households"]
    / (merged["Urban_Households"] + merged["Rural_Households"])
) * 100

if "Urbanization_Pct_Override" in merged.columns:
    merged["Urbanization_Pct"] = merged["Urbanization_Pct_Override"].combine_first(
        merged["Urbanization_Pct"]
    )

merged["Crime_Rate_Per_100k"] = (merged["Total"] / merged["Population"]) * 100000

st.subheader("📋 Merged District Data")
st.dataframe(
    merged[["Districts", "Population", "Urbanization_Pct", "Total", "Crime_Rate_Per_100k"]]
    .sort_values("Crime_Rate_Per_100k", ascending=False)
    .rename(columns={
        "Districts": "District",
        "Total": "Total Crime Cases",
        "Crime_Rate_Per_100k": "Crime Rate (per 100k)",
        "Urbanization_Pct": "Urbanization %"
    }),
    use_container_width=True
)

if not unmatched_crime.empty or not unmatched_pop.empty:
    with st.expander("⚠ Districts that couldn't be matched (click to review)"):
        if not unmatched_crime.empty:
            st.write("From crime data:", list(unmatched_crime["Districts"]))
        if not unmatched_pop.empty:
            st.write("From population data:", list(unmatched_pop["District name"]))
        st.caption("Add these to RENAME_MAP in the code if they represent the same district.")

st.divider()

# ---------------------------------------------------------
# STEP 4: Correlation scatter + AI insight
# ---------------------------------------------------------
st.subheader("📈 Urbanization vs Crime Rate")

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(merged["Urbanization_Pct"], merged["Crime_Rate_Per_100k"], color="#ff4b4b")

for _, row in merged.iterrows():
    ax.annotate(row["Districts"], (row["Urbanization_Pct"], row["Crime_Rate_Per_100k"]), fontsize=7)

ax.set_xlabel("Urbanization (%)")
ax.set_ylabel("Crime Rate (per 100k population)")
ax.set_title("Urbanization vs Crime Rate by District")

st.pyplot(fig)

if len(merged) >= 3:
    corr = np.corrcoef(merged["Urbanization_Pct"], merged["Crime_Rate_Per_100k"])[0, 1]

    if corr > 0.5:
        strength, direction = "a strong positive", "more urbanized districts tend to report notably higher crime rates"
    elif corr > 0.3:
        strength, direction = "a moderate positive", "more urbanized districts tend to report somewhat higher crime rates"
    elif corr > -0.3:
        strength, direction = "a weak / negligible", "urbanization alone does not clearly explain crime rate differences"
    elif corr > -0.5:
        strength, direction = "a moderate negative", "more urbanized districts tend to report somewhat lower crime rates"
    else:
        strength, direction = "a strong negative", "more urbanized districts tend to report notably lower crime rates"

    st.info(
        f"""
🤖 **AI Insight**

Correlation coefficient between urbanization and crime rate: **{corr:.2f}**

This indicates {strength} relationship — {direction} in this dataset.

Note: correlation does not imply causation. Other socio-economic factors
(policing intensity, reporting rates, population density, tourism, migration)
likely contribute to the observed pattern.
"""
    )
else:
    st.warning("Not enough matched districts to compute a reliable correlation.")

st.divider()
st.caption(
    "Data sources: 2011 Census of India (population, households) and Karnataka "
    "district-wise crime data (2023). Population figures are from the last "
    "available census and do not reflect current-year population changes."
)
