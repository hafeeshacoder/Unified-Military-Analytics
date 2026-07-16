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
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_excel("military_final.xlsx")


df = load_data()


# -----------------------------
# Title
# -----------------------------
st.title("🌍 Unified Military Analytics Dashboard")
st.subheader("Nation Overview Prototype")


# -----------------------------
# Check Dataset
# -----------------------------
st.success("Dataset Loaded Successfully")



# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Dashboard Filters")


country_column = "country"

if country_column in df.columns:

    country = st.sidebar.selectbox(
        "Select Country",
        sorted(df[country_column].dropna().unique())
    )

    selected = df[
        df[country_column] == country
    ]

else:
    st.error("Country column not found")
    st.stop()



# -----------------------------
# Country Heading
# -----------------------------
st.header(f"Military Overview : {country}")



# -----------------------------
# KPI Section
# -----------------------------

st.subheader("Key Performance Indicators")


available_columns = [
    "defense_budget",
    "total_aircraft",
    "active_personnel",
    "power_index",
    "assets_per_capita",
    "budget_to_gdp_ratio"
]


kpi_columns = []

for col in available_columns:
    if col in df.columns:
        kpi_columns.append(col)



cols = st.columns(len(kpi_columns))


for i, col in enumerate(kpi_columns):

    value = selected[col].iloc[0]

    cols[i].metric(
        col.replace("_"," ").title(),
        value
    )



# -----------------------------
# Military Assets Chart
# -----------------------------

st.subheader("Military Assets")


asset_columns = [
    "total_aircraft",
    "tanks",
    "naval_assets"
]


available_assets = []

for col in asset_columns:
    if col in df.columns:
        available_assets.append(col)



if len(available_assets) > 0:

    asset_data = selected[available_assets].T.reset_index()

    asset_data.columns=[
        "Asset",
        "Value"
    ]


    fig = px.bar(
        asset_data,
        x="Asset",
        y="Value",
        title="Military Asset Strength"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# -----------------------------
# Region Comparison
# -----------------------------

if "region" in df.columns and "defense_budget" in df.columns:

    st.subheader("Regional Defense Budget Comparison")


    region_data = (
        df.groupby("region")
        ["defense_budget"]
        .sum()
        .reset_index()
    )


    fig2 = px.bar(
        region_data,
        x="region",
        y="defense_budget",
        title="Defense Budget by Region"
    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )



# -----------------------------
# Dataset View
# -----------------------------

with st.expander("View Selected Country Data"):

    st.dataframe(selected)



# -----------------------------
# Footer
# -----------------------------

st.markdown(
"""
---
**Module 4 Prototype**
Unified Military Analytics Dashboard  
Built using Python + Streamlit
"""
)
