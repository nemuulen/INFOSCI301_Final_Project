# 🌍 INFOSCI301 Final Project: Global Student Mobility Dashboard

## International Student Mobility Visualization Project

**Team Members**  
- Yiqing Wang  
- Nemuulen Togtbaatar  

## Project Overview
This project analyzes global trends in international student mobility by examining inbound and outbound student flows across countries over time.  
By integrating UNESCO Institute for Statistics (UIS) mobility data with World Bank GDP indicators, we explore the relationship between a country's economic status and its role in international education exchanges.

🔗 **Live App**: [infosci301finalproject.streamlit.app](https://infosci301finalproject-j34vzlrqpnbbp22g879wld.streamlit.app/?embed_options=dark_theme)

---

## 🔧 Deployment Details

This project was deployed using **Streamlit Community Cloud**, which allows for seamless integration with GitHub repositories and automatic deployment upon code updates.

### Deployment Steps:
1. **GitHub Repository**: The project's codebase is hosted on GitHub.
2. **Streamlit App File**: The main application file is `app.py`.
3. **Dependencies**: All required Python libraries are listed in `requirements.txt`.
4. **Configuration**: A `.streamlit/config.toml` file is included to customize the app's appearance, such as enabling the dark theme.
5. **Deployment**:
   - Sign in to [Streamlit Community Cloud](https://streamlit.io/cloud).
   - Connect your GitHub account and select the repository.
   - Choose the `app.py` file as the entry point.
   - Deploy the app, which will be accessible via a unique URL.

---

## 🛠️ Technical Stack

- **Programming Language**: Python
- **Data Manipulation**: `pandas`
- **Data Visualization**: `plotly`, `matplotlib`
- **Web Framework**: `streamlit`
- **Development Environment**: Google Colab, local IDEs
- **Version Control**: Git, GitHub

---

## ✅ Suggestions for Enhancement

To further improve the project, consider the following:

- **Interactive Filters**: Implement dropdowns or sliders to allow users to filter data by year, country, or region.
- **Responsive Design**: Ensure that visualizations are responsive and render well on various devices and screen sizes.
- **Performance Optimization**: Optimize data loading and processing to enhance app performance, especially for large datasets.
- **Accessibility**: Incorporate accessibility features to make the app usable for individuals with disabilities.
- **Documentation**: Expand the README to include detailed instructions on setting up the development environment and contributing to the project.

---

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
![Innovation Flowchart](Images/Innovation_Flowchart.jpg)
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

## Data Analysis: Overall Trends in International Student Migration (2000–2021)
![International Student Migration 2000-2021](Images/International_Student_Migration2000_2022.jpg)

Between 2000 and 2021, international student migration patterns underwent significant transformations, reflecting broader trends in globalization, economic development, and educational access.

In 2000, the landscape of international education was relatively concentrated. A small group of developed countries — particularly those in Western Europe, North America, and Oceania — acted as the primary destinations for mobile students. Inbound flows were modest in scale and largely limited to traditional education hubs like France, Germany, the United Kingdom, Australia, and the United States. Meanwhile, outbound flows from developing countries were present but relatively limited, both in volume and in geographic reach.

As the decade progressed, the 2010 snapshot revealed the early signs of a more interconnected world. A larger number of countries began to engage actively in sending and receiving students. Notably, China, India, and Southeast Asian nations exhibited growing outbound migration. Inbound hubs such as Australia and the UK expanded further, while Europe as a whole solidified its position as a central magnet for international students.

By 2021, international student mobility had not only intensified but diversified. Inbound flows into major economies became significantly larger, represented by the dramatic growth in bubble sizes. The United States, Australia, the United Kingdom, Germany, and Canada emerged as dominant global destinations. At the same time, China rose sharply as the world's largest sender of outbound students, followed by India and other Asian economies. Outbound migration patterns became more dispersed, no longer concentrated in a handful of nations but rather involving a wider range of countries from different regions.

Throughout these two decades, several overarching trends can be observed:
- **Expansion and Diversification**: Both the number of mobile students and the number of participating countries increased dramatically, reflecting a broader democratization of international education.
- **Economic Correlation**: Wealthier nations consistently attracted higher numbers of inbound students, suggesting that economic strength remains a key driver of educational migration.
- **Rise of Asia**: Asia shifted from being predominantly a source of outbound students to becoming a crucial player in shaping global mobility patterns, both as senders and increasingly as receivers.
- **Resilience Despite Challenges**: Even in the face of global disruptions such as the COVID-19 pandemic, the data shows sustained student flows in 2021, underscoring the resilience and continued demand for international education.

These findings highlight how global education has evolved into a complex, multi-directional network of opportunities — aligning closely with Sustainable Development Goal 4 (SDG 4), which advocates for inclusive and equitable quality education and the promotion of lifelong learning opportunities for all.

## Data Analysis: Major Student Flows (2022)

![Major Student Flows 2022](Images/Major_Student_Flows2022.jpg)
The 2022 international student flow map reveals several key insights:

- **Dominant Destinations**: The United States and the United Kingdom remain the largest receivers of international students. Thick lines represent major inflows from Asia, Europe, and Latin America.
- **Emerging Intra-Asia Mobility**: A significant volume of students is moving between Asian countries, particularly from India, Vietnam, and Bangladesh to destinations such as Japan, South Korea, and Malaysia. This trend highlights the strengthening role of regional education hubs in Asia.
- **European Educational Connectivity**: Europe shows dense internal student mobility, with strong educational exchanges between EU countries. Initiatives like Erasmus likely contribute to this vibrant intra-European student movement.
- **Latin American Patterns**: Latin American students, especially from Brazil, Colombia, and Argentina, predominantly head toward the United States and Spain for higher education opportunities.
- **Access Gaps**: Sparse outbound flows from Sub-Saharan Africa point to ongoing challenges in equitable access to international education pathways.
  
Overall, the 2022 snapshot visualizes a complex, multi-centered network of global student mobility, demonstrating both traditional and emerging educational migration routes.

## Data Analysis: Relationship Between GDP and Student Migration (2022)

![Relationship Between GDP and Student Migration 2022](Images/Relationship_Between_GDP_and_Student_Migration2022.jpg)
The scatter plot reveals several important trends between a country's economic strength and its international student flows:

- **Positive Correlation**: Generally, countries with higher GDP levels tend to have higher numbers of both inbound and outbound international students. This suggests that economic resources enable better access to education abroad and greater attractiveness as education destinations.
- **Top Economies Dominate**: Economies like the United States, China, Germany, and the United Kingdom are positioned in the upper right, indicating they are both major sources and hosts of international students.
- **Outbound Mobility from Developing Economies**: Several developing countries with moderate GDPs (e.g., India, Vietnam, Nigeria) show relatively high outbound student numbers, reflecting strong demand for education abroad despite economic constraints.
- **Inbound Disparities**: Some wealthy countries have relatively fewer inbound students compared to their GDP size, suggesting that factors beyond economics—such as language, visa policies, or educational reputation—also impact inbound attractiveness.
- **Outliers and Exceptions**: A few smaller economies (e.g., Malaysia, the UAE) punch above their 
