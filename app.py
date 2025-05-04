from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import requests

# ─── Page config & navigation ───
st.set_page_config(
    page_title="Global Student Mobility Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)
section = st.sidebar.radio(
    "📂 Navigate to",
    ["Migration Animation", "Major Flows Map", "GDP vs Students"]
)

DATA_DIR = Path("data")

# ─── Utility: find a column by substring(s) ───
def find_col(df, *candidates):
    cols = df.columns
    lower = [c.lower() for c in cols]
    for cand in candidates:
        for i,name in enumerate(lower):
            if cand.lower() in name:
                return cols[i]
    return None

# ─── 1) Read World Bank Excel/CSV robustly ───
def read_wb(path: Path, var_name: str) -> pd.DataFrame:
    if path.suffix.lower().endswith(("xls","xlsx")):
        xls = pd.ExcelFile(path)
        df = pd.read_excel(xls, sheet_name=0, header=None)
        df.columns = df.iloc[4]
        df = df.iloc[5:].rename(columns={df.columns[0]:"Country", df.columns[1]:"Country Code"})
    else:
        df = pd.read_csv(path)
        # rename common variants
        if "Country Name" in df.columns:
            df = df.rename(columns={"Country Name":"Country"})
        if "Country_Code" in df.columns and "Country Code" not in df.columns:
            df = df.rename(columns={"Country_Code":"Country Code"})
    # melt year columns
    df = df.melt(id_vars=["Country","Country Code"], var_name="Year", value_name=var_name)
    # coerce year, drop NaNs, then int
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df.dropna(subset=["Year"])
    df["Year"] = df["Year"].astype(int)
    # coerce values
    df[var_name] = pd.to_numeric(df[var_name], errors="coerce")
    return df

# ─── 2) Load & clean migration data ───
def load_migration_data():
    gdp = read_wb(DATA_DIR/"GDP.csv", "GDP_USD")

    cm = pd.read_csv(DATA_DIR/"Country_names.csv")
    cm = cm.rename(columns={
        find_col(cm,"country_id"):"Country Code",
        find_col(cm,"country_name"):"Country"
    })

    inb = pd.read_csv(DATA_DIR/"inbound_intl.csv")
    inb = inb.rename(columns={
        find_col(inb,"geo"):"Country Code",
        find_col(inb,"year"):"Year",
        find_col(inb,"value"):"Inbound"
    })
    inb["Year"] = pd.to_numeric(inb["Year"], errors="coerce").astype(int)
    inb["Inbound"] = pd.to_numeric(inb["Inbound"], errors="coerce")
    inb = inb.merge(cm, on="Country Code")[["Country","Year","Inbound"]]

    net = pd.read_csv(DATA_DIR/"inbound-outbound_intl.csv")
    net = net.rename(columns={
        find_col(net,"geo"):"Country Code",
        find_col(net,"year"):"Year",
        find_col(net,"value"):"Net"
    })
    net["Year"] = pd.to_numeric(net["Year"], errors="coerce").astype(int)
    net["Net"] = pd.to_numeric(net["Net"], errors="coerce")
    net = net.merge(cm, on="Country Code")[["Country","Year","Net"]]

    df = inb.merge(net, on=["Country","Year"])
    df["Outbound"] = (df["Inbound"] - df["Net"]).clip(lower=0)
    df = df.merge(gdp, on=["Country","Year"], how="left")
    df = df[df["Year"].between(2000,2021)]

    df["GDP_text"] = df["GDP_USD"].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")

    long = df.melt(
        id_vars=["Country","Year","GDP_text"],
        value_vars=["Inbound","Outbound"],
        var_name="Type",
        value_name="Students"
    ).query("Students>=0")
    long["Year"] = long["Year"].astype(str)
    return long

# ─── 3) Load & clean flows map data ───
def load_flows_map():
    share = pd.read_csv(DATA_DIR / "Share_students_origin_to_destination.csv", encoding="ISO-8859-1")
    share = share.rename(columns={
        "REF_AREA": "Origin_Code",
        "Origin": "Origin",
        "Destination": "Destination",
        "TIME_PERIOD": "Year",
        "Percentage_of_students": "Share_pct"
    })
    share["Share_pct"] = pd.to_numeric(share["Share_pct"], errors="coerce")
    share = share.dropna(subset=["Origin_Code", "Origin", "Destination", "Share_pct"])

    total = pd.read_csv(DATA_DIR / "Total_num_students_going_abroad.csv", encoding="ISO-8859-1")
    total = total.rename(columns={
        "REF_AREA": "Origin_Code",
        "TOTAL_STUDENTS": "Total_Outbound"
    })
    total["Total_Outbound"] = pd.to_numeric(total["Total_Outbound"], errors="coerce")
    total = total.dropna(subset=["Origin_Code", "Total_Outbound"])

    df = pd.merge(share, total[["Origin_Code", "Total_Outbound"]], on="Origin_Code", how="inner")
    df["Flow"] = df["Total_Outbound"] * df["Share_pct"] / 100.0

    # Load coordinates
    resp = requests.get("https://restcountries.com/v3.1/all").json()
    iso3_to_latlon, iso3_to_continent, name_to_iso3 = {}, {}, {}

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
        key = str(code_or_name).strip()
        return iso3_to_latlon.get(key.upper()) or iso3_to_latlon.get(name_to_iso3.get(key))

    def resolve_continent(code_or_name):
        key = str(code_or_name).strip()
        return iso3_to_continent.get(key.upper()) or iso3_to_continent.get(name_to_iso3.get(key), "Other")

    coords = df.apply(lambda r: pd.Series({
        "o_ll": resolve_latlon(r["Origin_Code"]),
        "d_ll": resolve_latlon(r["Destination"]),
        "continent": resolve_continent(r["Origin_Code"])
    }), axis=1)

    df = pd.concat([df, coords], axis=1).dropna(subset=["o_ll", "d_ll"])
    return df.query("Flow > 1000")

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
# ────────────────────────────────────────────────────────────────────────────────
# Section 1: Migration Animation
if section=="Migration Animation":
    st.header("🌐 Animated Migration Bubbles (2000–2021)")
    long = load_migration_data()
    long = load_migration_data()
    long["Year"] = long["Year"].astype(int)
    long = long.sort_values("Year")
    long["Year"] = long["Year"].astype(str)  # Keep as string for animation_frame
    fig = px.scatter_geo(
        long, locations="Country", locationmode="country names",
        size="Students", color="Type", animation_frame="Year",
        color_discrete_map={"Inbound":"#1E90FF","Outbound":"#FF69B4"},
        hover_name="Country", hover_data={"Students":":,","GDP_text":True},
        projection="equirectangular", template="plotly_dark",
        fitbounds="locations", size_max=50,
        title="Animated International Student Migration"
    )
    fig.update_traces(marker=dict(opacity=0.7, line_width=0.5, line_color="white"))
    fig.update_layout(
    geo=dict(
        showcountries=True,
        center=dict(lat=0, lon=0),
    ),
    margin=dict(l=0, r=0, t=50, b=0),
    height=600
)
    st.plotly_chart(fig, use_container_width=True)


    # --- Top 10 Outbound Countries (2021) ---
    st.subheader("📊 Top 10 Outbound Countries (2021)")
    top_outbound = long.query("Year == '2021' and Type == 'Outbound'").nlargest(10, "Students")
    top_inbound = long.query("Year == '2021' and Type == 'Inbound'").nlargest(10, "Students")
    fig_outbound = px.bar(
        top_outbound.sort_values("Students"),
        x="Students",
        y="Country",
        orientation="h",
        title="Top 10 Outbound Countries (2021)",
        template="plotly_dark",
        labels={"Students": "Number of Students", "Country": "Country"}
    
    )
    st.plotly_chart(fig_outbound, use_container_width=True)

    # --- Top 10 Inbound Countries (2021) ---
    st.subheader("📊 Top 10 Inbound Countries (2021)")
    top_inbound["Country"] = top_inbound["Country"].str.slice(0, 24)  # truncate labels
    fig_inbound = px.bar(
        top_inbound.sort_values("Students"),
        x="Students",
        y="Country",
        orientation="h",
        title="Top 10 Inbound Countries (2021)",
        template="plotly_dark",
        labels={"Students": "Number of Students", "Country": "Country"}
    )
    st.plotly_chart(fig_inbound, use_container_width=True)

# Section 2: Major Flows Map
elif section=="Major Flows Map":
    st.header("🗺️ Major Student Flows (2022)")
    st.subheader("Student flows over 1000 students")
    dfm = load_flows_map()
    colors = {"Asia":"#CF9FFF","Europe":"#1E90FF","Africa":"green",
              "Oceania":"orange","Americas":"#FF69B4","Other":"gray"}
    fig2 = go.Figure()
    maxf = dfm["Flow"].max()
    for _,r in dfm.iterrows():
        lat0,lon0=r["o_ll"]; lat1,lon1=r["d_ll"]
        w = max(1,(r["Flow"]/maxf)*8)
        c = colors.get(r["continent"],"gray")
        fig2.add_trace(go.Scattergeo(
            lon=[lon0,lon1], lat=[lat0,lat1], mode="lines",
            line=dict(width=w,color=c), opacity=0.7,
            text=f"{r['Origin']} → {r['Destination']}<br>{int(r['Flow']):,}", hoverinfo="text"
        ))
    fig2.update_layout(
        template="plotly_dark",
        geo=dict(projection_type="equirectangular",
                 landcolor="black", oceancolor="black", countrycolor="white",
                 showcountries=True),
        margin=dict(l=0,r=0,t=50,b=0),
        height=600,
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 🌍 Continent Colors Legend", help="Continent color key of where the flow is originated.")
    for continent, color in colors.items():
        st.markdown(f"<span style='display:inline-block;width:12px;height:12px;background-color:{color};margin-right:10px;border-radius:50%;'></span>{continent}", unsafe_allow_html=True)

    st.subheader("📊 Top 10 Routes by Volume")
    top10 = dfm.nlargest(10,"Flow").copy()
    top10["Route"] = top10["Origin"] + " → " + top10["Destination"]
    bar = px.bar(
        top10.sort_values("Flow"), x="Flow", y="Route",
        orientation="h", template="plotly_dark",
        labels={"Flow":"Students","Route":"Route"},
        title="Top 10 Student Migration Routes (2022)"
    )
    st.plotly_chart(bar, use_container_width=True)

# Section 3: GDP vs Students Scatter 
elif section == "GDP vs Students":
    st.header("Relationship Between GDP and Student Migration (2022)")
    fig3 = make_gdp_vs_students_scatter()
    st.plotly_chart(fig3, use_container_width=True, height=700)
    st.markdown("""
    **Description:**  
    This scatter plot explores the relationship between a country's GDP and the number of students migrating internationally in 2022.
    """)

    # Forecast Student Migration with GDP
    st.subheader("📈 Forecast Student Migration with GDP (2000–2030)")

    # Load data
    df_full = load_migration_data()
    df = df_full.copy()
    df["Year"] = df["Year"].astype(int)

    # Dropdown for country selection
    countries = sorted(df["Country"].unique())
    selected_country = st.selectbox("Select a Country for Detailed Trend", countries)

    # Filter for selected country
    country_df = df[df["Country"] == selected_country]
    gdp_path = DATA_DIR / "GDP.csv"
    gdp_df = read_wb(gdp_path, "GDP_USD")
    gdp_country = gdp_df[gdp_df["Country"].str.strip() == selected_country.strip()]

    # Pivot student types
    pivot = country_df.pivot(index="Year", columns="Type", values="Students").fillna(0)
    gdp_vals = gdp_country.set_index("Year")["GDP_USD"].reindex(pivot.index).bfill()

    # Forecast up to 2030
    pivot.index = pivot.index.astype(int)
    all_years = np.arange(pivot.index.min(), 2031)
    forecast_dfs = []

    for col in ["Inbound", "Outbound"]:
        if col not in pivot.columns:
            continue
        real_vals = pivot[col]
        coeffs = np.polyfit(real_vals.index.values, real_vals.values, 1)
        preds = np.polyval(coeffs, all_years)

        df_col = pd.DataFrame({
            "Year": all_years,
            "Students": preds,
            "Type": col,
            "IsForecast": ~np.isin(all_years, real_vals.index.values)
        })
        forecast_dfs.append(df_col)

    df_students = pd.concat(forecast_dfs, ignore_index=True)

    # GDP Forecast
    if not gdp_vals.dropna().empty:
        gdp_coeff = np.polyfit(gdp_vals.index.values, gdp_vals.values, 1)
        gdp_preds = np.polyval(gdp_coeff, all_years)
        gdp_forecast = pd.DataFrame({
            "Year": all_years,
            "GDP_USD": gdp_preds,
            "IsForecast": ~np.isin(all_years, gdp_vals.index.values)
        })
    else:
        gdp_forecast = pd.DataFrame(columns=["Year", "GDP_USD", "IsForecast"])

    # Plotting
    fig = go.Figure()

    for t in ["Inbound", "Outbound"]:
        df_t = df_students[df_students["Type"] == t]
        color = "#1E90FF" if t == "Inbound" else "#FF69B4"

        df_real = df_t[~df_t["IsForecast"]]
        df_fore = df_t[df_t["IsForecast"]]

        fig.add_trace(go.Scatter(
            x=df_real["Year"], y=df_real["Students"],
            mode="lines+markers", name=f"{t} (Actual)",
            line=dict(color=color, dash="solid"), marker=dict(symbol="circle")
        ))
        fig.add_trace(go.Scatter(
            x=df_fore["Year"], y=df_fore["Students"],
            mode="lines+markers", name=f"{t} (Estimated)",
            line=dict(color=color, dash="dot"), marker=dict(symbol="circle")
        ))

    if not gdp_forecast.empty:
        df_real_gdp = gdp_forecast[~gdp_forecast["IsForecast"]]
        df_fore_gdp = gdp_forecast[gdp_forecast["IsForecast"]]

        fig.add_trace(go.Scatter(
            x=df_real_gdp["Year"], y=df_real_gdp["GDP_USD"],
            name="GDP (Actual)", yaxis="y2",
            line=dict(color="white", dash="solid")
        ))
        fig.add_trace(go.Scatter(
            x=df_fore_gdp["Year"], y=df_fore_gdp["GDP_USD"],
            name="GDP (Estimated)", yaxis="y2",
            line=dict(color="white", dash="dot")
        ))

    fig.update_layout(
        template="plotly_dark",
        title=f"{selected_country}: Forecast of Student Migration and GDP",
        xaxis=dict(title="Year"),
        yaxis=dict(title="Students"),
        yaxis2=dict(title="GDP (USD)", overlaying="y", side="right", type="log"),
        legend=dict(x=0.02, y=1.05),
        margin=dict(l=20, r=20, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Data sources: UNESCO Institute for Statistics, World Bank, REST Countries API")