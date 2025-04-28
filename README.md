# INFOSCI301_Final_Project

## International Student Mobility Visualization Project

**Team Members**  
- Yiqing Wang  
- Nemuulen Togtbaatar  

## Project Overview
This project analyzes global trends in international student mobility by examining inbound and outbound student flows across countries over time.  
By integrating UNESCO Institute for Statistics (UIS) mobility data with World Bank GDP indicators, we explore the relationship between a country's economic status and its role in international education exchanges.

https://infosci301finalproject-j34vzlrqpnbbp22g879wld.streamlit.app/?embed_options=dark_theme

## Research Questions
- Which countries are the largest senders and receivers of international students, and how does this correlate with their GDP?
- How have student mobility patterns evolved over the past two decades, particularly in relation to economic changes?
- Are there identifiable regional trends in student migration linked to economic indicators?

## Scholarly Grounding
We draw design inspiration from:

> Schöttler, S., Hinrichs, U., & Bach, B. (2025).  
> *Practices and Strategies in Responsive Thematic Map Design.*  
> IEEE Transactions on Visualization and Computer Graphics (TVCG).

This paper highlights challenges in thematic map design — such as overlapping symbols, navigation difficulties, and loss of context — and suggests strategies like dynamic scaling and interactive features.  
Our project adapts these ideas to create accessible, responsive migration visualizations.

## Workflow Pipeline
- **Data Acquisition**: Sources include World Bank, UNESCO UIS, and OECD datasets.
- **Data Cleaning**: Handling missing values, reshaping wide/long formats, matching country names.
- **Visualization Planning**: Identifying key metrics (GDP, inbound/outbound numbers) and appropriate visualization types.
- **Visualization Coding**: Using Python libraries (pandas, plotly) and Google Colab for iterative development.
- **Data Analysis**: Exploring trends, regional differences, and economic correlations.
- **Report and Deployment**: Documenting findings on GitHub with organized codes, results, and a project poster.

## Datasets Used
| Dataset | Source |
|:--------|:-------|
| **GDP.xlsx** | [World Bank GDP Data](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD) |
| **Government expenditure on education as % of GDP (%)** | [World Bank Education Expenditure](https://data.worldbank.org/indicator/SE.XPD.TOTL.GD.ZS) |
| **Country_names.xlsx** | UNESCO UIS (self-created lookup) |
| **inbound and outbound of international students.xlsx** | [UNESCO UIS Data](https://uis.unesco.org/bdds) |
| **Total inbound internationally mobile students, both sexes (number).xlsx** | [UNESCO UIS Data](https://uis.unesco.org/bdds) |
| **Share_students_origin_to_destination.xlsx** | [OECD Data Explorer](https://data-explorer.oecd.org) |
| **Total_num_students_going_abroad.xlsx** | [OECD Data Explorer](https://data-explorer.oecd.org) |

> *Note*: China's outbound numbers were computed based on the last two datasets.

## Visualizations
- **Main Animated Map**: Displays changing inbound and outbound student volumes globally from 2000–2022.
- **GDP vs Students Scatter Plot**: Shows correlation between GDP and student mobility numbers across countries over time.
- **2022 Flows Map**: Focuses on 2022 only, visualizing student flows between origin and destination countries via connecting lines.

## Connection to SDG 4 (Quality Education)
This project contributes to SDG 4 by:
- Highlighting global disparities in access to international education.
- Promoting data-driven awareness of trends in educational migration.
- Supporting conversations around equity in educational opportunities and resources worldwide.

By visualizing these mobility trends, our project encourages actions toward **promoting equitable access to international education opportunities**.

## Team Contribution Statement
- **Yiqing Wang**: Data acquisition, data visualization, GitHub repository development.
- **Nemuulen Togtbaatar**: Data acquisition and cleaning, literature review, visualization improvements.
