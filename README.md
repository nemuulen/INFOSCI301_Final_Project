# INFOSCI301_Final_Project

# INFOSCI 301 – Team Research Proposal  
## Mapping Global Student Migration Patterns in Relation to Economic Indicators

**Team Members**  
- Yiqing Wang  
- Nemuulen Togtbaatar  

---

## 1. Project Overview  
This project analyzes global trends in international student mobility by examining inbound and outbound student flows across countries over time. By integrating data from the UNESCO Institute for Statistics (UIS) on international student mobility with GDP, education‐expenditure and urbanization data from the World Bank, we seek to explore the relationship between a country’s economic status and its role in international education exchanges.

---

## 2. Research Questions  
1. Which countries are the largest **senders** and **receivers** of international students, and how does this correlate with their GDP?  
2. How have global student mobility patterns evolved over the past decade, particularly in relation to economic growth or decline?  
3. Are there identifiable **regional trends** in student migration linked to economic indicators?

---

## 3. Data Sources & Integration  

| Source                              | Indicator                                               | URL                                                                                   |
|-------------------------------------|---------------------------------------------------------|---------------------------------------------------------------------------------------|
| **UNESCO Institute for Statistics** | International student mobility (inbound & outbound)     | https://uis.unesco.org/bdds                                                           |
| **World Bank**                      | GDP (current US$)                                       | https://data.worldbank.org/indicator/NY.GDP.MKTP.CD                                   |
| **World Bank**                      | Government expenditure on education (% of GDP)          | https://data.worldbank.org/indicator/SE.XPD.TOTL.GD.ZS                                |
| **World Bank**                      | Urban population (% of total population)                | https://data.worldbank.org/indicator/SP.URB.TOTL.IN.ZS                                |

---

## 4. Methodology & Visualization Plan  

### Tools  
- **Python 3.7+**  
  - `pandas` for data wrangling  
  - `plotly.express` for animated globe maps  
  - `pathlib` for portable file paths  
  - `openpyxl` (via pandas) to read Excel  
- **Google Colab** as execution environment  
- **GitHub** for version control & reproducibility  

### Planned Visualizations  
- **Animated bubble‐map** (2000–2022):  
  - Blue bubbles = inbound students  
  - Red bubbles = outbound students  
  - Bubble size ∝ student count  
- **Choropleth overlays** to color‐code by GDP or education expenditure  
- **Interactive pop‐up panels** showing country‐specific line charts of GDP, education %, and urbanization  

---

## 5. Innovation Pipeline Flowchart  

```mermaid
flowchart LR
  A[Data Acquisition] --> B[Data Cleaning]
  B --> C[Data Integration]
  C --> D[Exploratory Analysis]
  D --> E[Design & Prototyping]
  E --> F[Visualization Development]
  F --> G[Deployment & User Testing]
