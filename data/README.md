## Project dataset overview
By integrating UNESCO Institute for Statistics (UIS) mobility data with World Bank GDP indicators, we explore the relationship between a country's economic status and its role in international education exchanges. The data principles of the UNESCO Institute for Statistics (UIS) and the World Bank emphasize openness, quality, accessibility, interoperability, and transparency, ensuring that data is freely available, methodologically sound, standardized across countries, and clearly documented to support informed decision-making and accountability. We have also integrated datasets from the OECD (Organisation for Economic Co-operation and Development) to show the international student migration flows all over the world.


## 📁 Datasets Used

| Dataset | Source |
|--------|--------|
| GDP.csv | [World Bank GDP](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD) |
| Government expenditure on education as % of GDP (%).csv | [World Bank GDP](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD) |
| inbound-outbound_intl.csv | [UNESCO UIS](https://uis.unesco.org/) |
| inbound_intl.csv | [UNESCO UIS](https://uis.unesco.org/) |
| Share_students_origin_to_destination.csv | [OECD](https://data-explorer.oecd.org) |
| Total_num_students_going_abroad.csv | [OECD](https://data-explorer.oecd.org) |
| Country_names.csv | [OECD](https://data-explorer.oecd.org) |
| RAW_inbound_and_outbound_data.csv | [UNESCO UIS](https://uis.unesco.org/)  |

## Data cleaning and adjustments
We first used the data search tool from the UN and the World Bank and filtered out the data. Then we have changed the file and column names and deleted useless information for better understandability. Then, for the datasets found from OECD, we have manually adjusted some country names that had syntax errors. 
