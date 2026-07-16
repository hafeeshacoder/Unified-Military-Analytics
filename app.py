import streamlit as st
import pandas as pd
import plotly.express as px


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Unified Military Analytics Dashboard",
    page_icon="🌍",
    layout="wide"
)


# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_excel("military_final.xlsx")


df = load_data()


# -----------------------------
# Header
# -----------------------------
st.title("🌍 Unified Military Analytics Dashboard")
st.markdown("### Nation Overview - Military Power Analysis")


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("🔎 Filters")


if "country" not in df.columns:
    st.error("Country column not found in dataset")
    st.stop()


country = st.sidebar.selectbox(
    "Select Country",
    sorted(df["country"].dropna().unique())
)


selected = df[df["country"] == country]


# -----------------------------
# KPI CARDS
# -----------------------------

st.subheader(f"📌 {country} Key Metrics")


kpis = [
    ("Defense Budget", "defense_budget"),
    ("Total Aircraft", "total_aircraft"),
    ("Active Personnel", "active_personnel"),
    ("Power Index", "power_index"),
    ("Assets per Capita", "assets_per_capita"),
    ("Budget GDP Ratio", "budget_to_gdp_ratio")
]


available_kpis = [
    k for k in kpis
    if k[1] in df.columns
]


columns = st.columns(len(available_kpis))


for i, (name, col) in enumerate(available_kpis):

    value = selected[col].iloc[0]

    columns[i].metric(
        name,
        value
    )


# -----------------------------
# Military Assets Chart
# -----------------------------

st.divider()

st.subheader("⚔️ Military Assets")


asset_list = [
    "total_aircraft",
    "tanks",
    "naval_assets"
]


available_assets = [
    x for x in asset_list
    if x in df.columns
]


if available_assets:

    asset_values = []

    for asset in available_assets:

        asset_values.append(
            {
                "Asset": asset.replace("_"," ").title(),
                "Value": selected[asset].iloc[0]
            }
        )


    asset_df = pd.DataFrame(asset_values)


    fig = px.bar(
        asset_df,
        x="Asset",
        y="Value",
        text="Value",
        title="Military Asset Strength"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


else:

    st.warning(
        "No military asset columns available"
    )


# -----------------------------
# Region Comparison
# -----------------------------

if "region" in df.columns and "defense_budget" in df.columns:


    st.divider()

    st.subheader("🌎 Defense Budget by Region")


    region_df = (
        df.groupby("region")
        ["defense_budget"]
        .sum()
        .reset_index()
    )


    fig2 = px.bar(
        region_df,
        x="region",
        y="defense_budget",
        title="Regional Defense Budget"
    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )


# -----------------------------
# Data Table
# -----------------------------

st.divider()

with st.expander("📄 View Country Data"):

    st.dataframe(
        selected,
        use_container_width=True
    )


# -----------------------------
# Footer
# -----------------------------

st.markdown(
"""
---
### Module 4 Prototype
Built using:
- Python
- Streamlit
- Pandas
- Plotly

Features:
✔ Interactive country filter  
✔ KPI cards  
✔ Military asset visualization  
✔ Economic comparison
"""
)
