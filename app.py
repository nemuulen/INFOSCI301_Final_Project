from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

# Set page title
st.set_page_config(
    page_title="International Student Migration",
    layout="wide"
)

# DATA_DIR should point to your local `data/` folder
DATA_DIR = Path("data")

# --- Read and prepare data ---
def load_data():
    def read_wb(path: Path, var_name: str) -> pd.DataFrame:
        xls = pd.ExcelFile(path)
        df = pd.read_excel(xls, sheet_name=xls.sheet_names[0], header=None)
        df.columns = df.iloc[4]
        df = df.iloc[5:].rename(columns={
            df.columns[0]: "Country",
            df.columns[1]: "Country Code"
        })
        df = df.melt(
            id_vars=["Country", "Country Code"],
            var_name="Year",
            value_name=var_name
        )
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
        df[var_name] = pd.to_numeric(df[var_name], errors="coerce")
        return df.dropna(subset=["Year"])

    gdp = read_wb(DATA_DIR / "GDP.xlsx", "GDP_USD")
    edu = read_wb(DATA_DIR / "Government expenditure on education as % of GDP (%).xlsx", "Edu_pct_GDP")
    urban = read_wb(DATA_DIR / "Urban population (% of total population).xlsx", "Urban_pct")

    country_map = pd.read_excel(DATA_DIR / "Country_names.xlsx").rename(
        columns={"COUNTRY_ID": "Country Code", "COUNTRY_NAME_EN": "Country"}
    )

    raw = pd.read_excel(DATA_DIR / "inbound and outbound of international students.xlsx", sheet_name="data")
    flows = {26637: "Inbound", 26519: "Outbound"}

    mig = (
        raw[raw["indicatorId"].isin(flows)]
        .rename(columns={"geoUnit": "Country Code", "year": "Year", "value": "Students"})
        .assign(
            Type=lambda df: df["indicatorId"].map(flows),
            Year=lambda df: pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
        )
        .dropna(subset=["Year", "Students"])
        .merge(country_map, on="Country Code", how="left")
        .dropna(subset=["Country"])
    )

    mig_wide = (
        mig.pivot_table(index=["Country", "Year"], columns="Type", values="Students", aggfunc="first")
        .reset_index()
    )

    df = (
        mig_wide
        .merge(gdp, on=["Country", "Year"], how="left")
        .merge(edu, on=["Country", "Year"], how="left")
        .merge(urban, on=["Country", "Year"], how="left")
    )

    df = df[df["Year"].between(2000, 2022)]

    long = (
        df.melt(
            id_vars=["Country", "Year", "GDP_USD", "Edu_pct_GDP", "Urban_pct"],
            value_vars=["Inbound", "Outbound"],
            var_name="Type",
            value_name="Students"
        )
        .dropna(subset=["Students"])
    )
    long["Year"] = long["Year"].astype(str)
    return long

# --- Main Streamlit App ---
st.title("🌐 International Student Migration Dashboard")
st.markdown("Visualizing global student mobility patterns from 2000 to 2022")

# Load data
with st.spinner("Loading data..."):
    long = load_data()

# Add year selection slider
years = sorted(long["Year"].unique())
selected_year = st.select_slider(
    "Select Year",
    options=years,
    value=years[-1]  # Default to most recent year
)

# Filter data for selected year
filtered_data = long[long["Year"] == selected_year]

# Create visualization
color_map = {"Inbound": "blue", "Outbound": "red"}

fig = px.scatter_geo(
    filtered_data,
    locations="Country",
    locationmode="country names",
    size="Students",
    color="Type",
    color_discrete_map=color_map,
    hover_name="Country",
    hover_data={
        "Students": ":,",
        "GDP_USD": ":,.0f",
        "Edu_pct_GDP": ":.1f",
        "Urban_pct": ":.1f",
        "Type": False,
        "Year": False
    },
    projection="natural earth",
    size_max=40,
    template="plotly_white",
    title=f"International Student Migration in {selected_year}<br><sub>Blue = Inbound | Red = Outbound</sub>"
)

fig.update_traces(marker=dict(opacity=0.6, line_width=0.5, line_color="darkgrey"))
fig.update_geos(
    showcountries=True, countrycolor="lightgray",
    showland=True, landcolor="whitesmoke",
    showocean=True, oceancolor="lightblue"
)
fig.update_layout(
    margin=dict(l=0, r=0, t=70, b=0),
    legend_title_text="Flow Type",
    height=700  # Make the map larger
)

# Display the map
st.plotly_chart(fig, use_container_width=True)

# Add some additional information
st.markdown("---")
st.subheader("About this visualization")
st.markdown("""
This dashboard visualizes the global flow of international students. The data shows:
- **Inbound students** (blue): Foreign students coming into a country
- **Outbound students** (red): Domestic students going to study abroad
- **Bubble size**: Proportional to the number of students
- **Hover information**: Includes GDP, education expenditure, and urban population percentage
""")

# Add data source information
st.markdown("---")
st.caption("Data sources: UNESCO Institute for Statistics, World Bank")
