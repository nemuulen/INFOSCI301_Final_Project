from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import requests

# Set page title
st.set_page_config(
    page_title="International Student Migration Dashboard",
    layout="wide"
)

DATA_DIR = Path("data")

# --- Helper functions ---
def read_wb(path: Path, var_name: str) -> pd.DataFrame:
    if path.suffix.lower() in (".xls", ".xlsx"):
        xls = pd.ExcelFile(path)
        df = pd.read_excel(xls, sheet_name=xls.sheet_names[0], header=None)
        df.columns = df.iloc[4]
        df = df.iloc[5:].rename(columns={df.columns[0]: "Country", df.columns[1]: "Country Code"})
    else:
        df = pd.read_csv(path)
        df = df.rename(columns={"Country Name": "Country", "Country Code": "Country Code"})
        for col in ("Indicator Name", "Indicator Code"):
            if col in df.columns:
                df = df.drop(columns=col)
    df = df.melt(id_vars=["Country", "Country Code"], var_name="Year", value_name=var_name)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"])
    df["Year"] = df["Year"].astype(int)
    df[var_name] = pd.to_numeric(df[var_name], errors="coerce")
    return df

# --- Load migration data ---
def load_migration_data():
    gdp = read_wb(DATA_DIR / "GDP.csv", "GDP_USD")

    country_map = pd.read_csv(DATA_DIR / "Country_names.csv").rename(
        columns={"COUNTRY_ID": "Country Code", "COUNTRY_NAME_EN": "Country"}
    )

    inb = pd.read_csv(DATA_DIR / "inbound_intl.csv")\
        .rename(columns={"geoUnit": "Country Code", "year": "Year", "value": "Inbound"})
    inb["Year"] = pd.to_numeric(inb["Year"], errors="coerce").dropna().astype(int)
    inb["Inbound"] = pd.to_numeric(inb["Inbound"], errors="coerce")
    inb = (
        inb.merge(country_map, on="Country Code", how="left")
           .dropna(subset=["Country"])
           [["Country", "Country Code", "Year", "Inbound"]]
    )

    net = pd.read_csv(DATA_DIR / "inbound-outbound_intl.csv")\
        .rename(columns={"geoUnit": "Country Code", "year": "Year", "value": "Net"})
    net["Year"] = pd.to_numeric(net["Year"], errors="coerce").dropna().astype(int)
    net["Net"] = pd.to_numeric(net["Net"], errors="coerce")
    net = (
        net.merge(country_map, on="Country Code", how="left")
           .dropna(subset=["Country"])
           [["Country", "Country Code", "Year", "Net"]]
    )

    df_io = inb.merge(net, on=["Country", "Country Code", "Year"], how="inner")
    df_io["Outbound"] = (df_io["Inbound"] - df_io["Net"]).clip(lower=0)

    df = (
        df_io[["Country", "Year", "Inbound", "Outbound"]]
          .merge(gdp, on=["Country", "Year"], how="left")
    )

    df = df[df["Year"].between(2000, 2021)]

    df["GDP_text"] = df["GDP_USD"].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")

    long = df.melt(
        id_vars=["Country", "Year", "GDP_text"],
        value_vars=["Inbound", "Outbound"],
        var_name="Type",
        value_name="Students"
    ).dropna(subset=["Students"])
    long = long[long["Students"] >= 0]
    long["Year"] = long["Year"].astype(str)

    return long

# --- Load flows ---
def load_flows_map():
    share_fp = DATA_DIR / "Share_students_origin_to_destination.csv"
    total_fp = DATA_DIR / "Total_num_students_going_abroad.csv"

    share = pd.read_csv(share_fp)
    share = share.rename(columns={
        "REF_AREA": "Origin_Code",
        "TIME_PERIOD": "Year",
        "Percentage_of_students": "Share_pct"
    })
    share["Share_pct"] = pd.to_numeric(share["Share_pct"].astype(str).str.replace(",", "."), errors="coerce")
    share = share.dropna(subset=["Origin_Code", "Origin", "Destination", "Share_pct"])

    total = pd.read_csv(total_fp)
    total = total.rename(columns={
        "REF_AREA": "Origin_Code",
        "TOTAL_STUDENTS": "Total_Outbound"
    })
    total["Total_Outbound"] = pd.to_numeric(total["Total_Outbound"].astype(str).str.replace(",", "."), errors="coerce")
    total = total.dropna(subset=["Origin_Code", "Total_Outbound"])

    df = pd.merge(
        share,
        total[["Origin_Code", "Total_Outbound"]],
        on="Origin_Code",
        how="inner"
    )
    df["Flow"] = df["Total_Outbound"] * df["Share_pct"] / 100.0

    resp = requests.get("https://restcountries.com/v3.1/all").json()
    iso3_to_latlon = {}
    iso3_to_continent = {}
    name_to_iso3 = {}
    for c in resp:
        iso3 = c.get("cca3", "").upper()
        latlng = c.get("latlng", [])
        name = c.get("name", {}).get("common", "")
        continent = c.get("region", "Other")
        if iso3 and len(latlng) == 2:
            iso3_to_latlon[iso3] = latlng
            iso3_to_continent[iso3] = continent
        if name and iso3:
            name_to_iso3[name] = iso3

    def resolve_latlon(code_or_name):
        key = str(code_or_name)
        if key.upper() in iso3_to_latlon:
            return iso3_to_latlon[key.upper()]
        iso = name_to_iso3.get(key)
        if iso and iso in iso3_to_latlon:
            return iso3_to_latlon[iso]
        return None

    def resolve_continent(code_or_name):
        key = str(code_or_name)
        if key.upper() in iso3_to_continent:
            return iso3_to_continent[key.upper()]
        iso = name_to_iso3.get(key)
        if iso and iso in iso3_to_continent:
            return iso3_to_continent[iso]
        return "Other"

    coords = df.apply(lambda r: pd.Series({
        "origin_latlon": resolve_latlon(r["Origin_Code"]),
        "dest_latlon": resolve_latlon(r["Destination"]),
        "continent": resolve_continent(r["Origin_Code"])
    }), axis=1)

    df = pd.concat([df, coords], axis=1).dropna(subset=["origin_latlon", "dest_latlon"])
    df = df[df["Flow"] > 1000]

    return df

# --- GDP vs Students Scatter ---
def make_gdp_vs_students_scatter():
    gdp = read_wb(DATA_DIR / "GDP.csv", "GDP_USD")

    country_map = pd.read_csv(DATA_DIR / "Country_names.csv").rename(
        columns={"COUNTRY_ID": "Country Code", "COUNTRY_NAME_EN": "Country"}
    )

    inb = pd.read_csv(DATA_DIR / "inbound_intl.csv")\
        .rename(columns={"geoUnit": "Country Code", "year": "Year", "value": "Inbound"})
    inb["Year"] = pd.to_numeric(inb["Year"], errors="coerce").dropna().astype(int)
    inb["Inbound"] = pd.to_numeric(inb["Inbound"], errors="coerce")
    inb = (
        inb.merge(country_map, on="Country Code", how="left")
           .dropna(subset=["Country"])
           [["Country", "Country Code", "Year", "Inbound"]]
    )

    net = pd.read_csv(DATA_DIR / "inbound-outbound_intl.csv")\
        .rename(columns={"geoUnit": "Country Code", "year": "Year", "value": "Net"})
    net["Year"] = pd.to_numeric(net["Year"], errors="coerce").dropna().astype(int)
    net["Net"] = pd.to_numeric(net["Net"], errors="coerce")
    net = (
        net.merge(country_map, on="Country Code", how="left")
           .dropna(subset=["Country"])
           [["Country", "Country Code", "Year", "Net"]]
    )

    # Compute outbound
    df_io = inb.merge(net, on=["Country", "Country Code", "Year"], how="inner")
    df_io["Outbound"] = (df_io["Inbound"] - df_io["Net"]).clip(lower=0)

    df = (
        df_io[["Country", "Year", "Inbound", "Outbound"]]
          .merge(gdp, on=["Country", "Year"], how="left")
    )

    # --- Focus only on 2022
    df_2022 = df[df["Year"] == 2022].dropna(subset=["GDP_USD"])

    # --- Melt inbound and outbound separately
    long = df_2022.melt(
        id_vars=["Country", "GDP_USD"],
        value_vars=["Inbound", "Outbound"],
        var_name="Type",
        value_name="Students"
    ).dropna(subset=["Students"])
    long = long[long["Students"] >= 0]

    # --- Scatter plot
    color_map = {"Inbound": "#1E90FF", "Outbound": "#FF69B4"}

    fig2 = px.scatter(
        long,
        x="GDP_USD",
        y="Students",
        color="Type",
        color_discrete_map=color_map,
        size="Students",
        size_max=40,
        hover_name="Country",
        template="plotly_dark",
        labels={"GDP_USD": "GDP (USD)", "Students": "Students"},
        title="🌐 GDP vs Student Migration (2022)"
    )

    fig2.update_traces(marker=dict(opacity=0.6, line_color="darkgrey", line_width=0.5))
    fig2.update_layout(
        xaxis_type="log",
        yaxis_type="log",
        margin=dict(l=0, r=0, t=50, b=0),
        legend_title_text="Flow Type",
    )

    return fig2

# --- Streamlit Page ---
st.title("🌐 International Student Migration Dashboard")

# --- 1. Bubble Migration Map ---
st.header("Global Student Migration Bubbles (2000–2021)")
long = load_migration_data()
years = sorted(long["Year"].unique())
selected_year = st.select_slider("Select Year", options=years, value=years[-1])

filtered_data = long[long["Year"] == selected_year]

fig1 = px.scatter_geo(
    filtered_data,
    locations="Country",
    locationmode="country names",
    size="Students",
    color="Type",
    color_discrete_map={"Inbound": "#1E90FF", "Outbound": "#FF69B4"},
    hover_name="Country",
    hover_data={"Students": ":,", "GDP_text": True, "Type": False, "Year": False},
    labels={"GDP_text": "GDP (USD)"},
    projection="natural earth",
    size_max=50,
    template="plotly_dark",
    title=f"International Student Migration in {selected_year}"
)

fig1.update_layout(
    margin=dict(l=0, r=0, t=50, b=0),
    height=900
)

fig1.update_traces(marker=dict(opacity=0.6, line_color="darkgrey", line_width=0.5))
st.plotly_chart(fig1, use_container_width=True, height=800)
st.markdown("""
**Description:**  
This map shows inbound and outbound international students by country. Bubble sizes represent the number of students moving during the selected year.
""")

# --- 2. Major Student Flows Map ---
st.header("Major International Student Flows (>1000 Students, 2022)")
df = load_flows_map()

continent_colors = {
    "Asia": "#CF9FFF",
    "Europe": "#1E90FF",
    "Africa": "green",
    "Oceania": "orange",
    "Americas": "#FF69B4",
    "Other": "gray"
}

fig2 = go.Figure()
max_flow = df["Flow"].max()

for _, r in df.iterrows():
    lat0, lon0 = r["origin_latlon"]
    lat1, lon1 = r["dest_latlon"]
    width = max(1.0, (r["Flow"] / max_flow) * 8)
    color = continent_colors.get(r["continent"], "gray")

    fig2.add_trace(go.Scattergeo(
        lon=[lon0, lon1],
        lat=[lat0, lat1],
        mode="lines",
        line=dict(width=width, color=color),
        hoverinfo="text",
        text=f"<b>From:</b> {r['Destination']}<br><b>To:</b> {r['Origin']}<br><b>Students:</b> {int(r['Flow']):,}",
        showlegend=False
    ))

fig2.update_layout(
    title_text="Major Student Flows (2022)",
    geo=dict(projection_type="natural earth", showcountries=True, countrycolor="lightgray",
             showland=True, landcolor="black", showocean=True, oceancolor="black"),
    margin=dict(l=0, r=0, t=50, b=0),
    showlegend=False,
    height=900
)

fig2.update_layout(
    template="plotly_dark",
    plot_bgcolor="black",
    margin=dict(l=0, r=0, t=50, b=0),
    showlegend=False
)

st.plotly_chart(fig2, use_container_width=True, height=800)
st.markdown("""
**Description:**  
This flow map highlights major student migration routes in 2022, showing only movements with more than 1000 students.
""")

# --- 3. GDP vs Students Scatter ---
st.header("Relationship Between GDP and Student Migration (2022)")
fig3 = make_gdp_vs_students_scatter()
st.plotly_chart(fig3, use_container_width=True, height=700)
st.markdown("""
**Description:**  
This scatter plot explores the relationship between a country's GDP and the number of students migrating internationally in 2022.
""")

# Footer
st.markdown("---")
st.caption("Data sources: UNESCO Institute for Statistics, World Bank")