# Project Plan for IS 477 Course Final Project

This document serves as the document plan outlining Team, Research Question, Dataset, Timeline, Constraints, Gaps of the project. 

## Overview
This project investigates the intersection of public health crises and capital markets by analyzing the relationship between COVID-19 severity and the financial performance of the U.S. pharmaceutical sector from January 1, 2021, to January 1, 2022.

To achieve this, we will develop a unified analytical pipeline that integrates high-resolution health data from the Johns Hopkins COVID-19 repository with financial time-series data extracted via the yfinance API. The technical execution will involve using SQL for robust data relational mapping and Python libraries, specifically Pandas, for complex data wrangling and feature engineering. Furthermore, we will implement machine learning models using scikit-learn to identify predictive patterns and quantify the sensitivity of pharmaceutical stocks to pandemic-driven news cycles.



## Team
1. **Yuhan Zhou**

    Yuhan Zhou is responsible for checking the data profile by describing its structure, content, and characteristics of each dataset. She need to specify the location of the dataset files in the project directory and discuss any ethical or legal constraints associated with the data and explain how the dataset relate to the research question. She will also be responsible of the ensuring the data quality, and done the data cleaning operation and explain how each operation addressed specific data quality issues. 

2. **Bowen Zhao**

    Bowen Zhao is responsible for data analysis including numeric results and visualizations based on the research question. After the analysis, he would also be responsible for a brief discussion about the lessons learned from the data analysis and potential future work. He will also be responsible for describing challenges encountered during the process.

Both group mates are responsible for brainstorming the research questions and dataset finding. 

## Research Question

In the end of 2019 and the start of 2020, the outbreak of COVID-19 has fundamentally changed the world for individuals, companies, and countries. As a biological incident, the coronavirus's impact on pharmaceutical companies capture the interests of our group. We are curious as the threat of COVID-19 became more evident and dreadful, how did this change impacted the performance of pharmaceutical companies. Considering the scope of this course, we formed our research question as:

> ***What is the relationship between the stock prices of pharmaceutical companies from Jan. 1, 2021 to Jan. 1, 2022 and the number of confirmed cases and death of COVID-19 in the U.S.?***

## Dataset

Two datasets are used in this project: the COVID-19 dataset by John Hopkins University and the stock prices dataset by yfinance.

1. **COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University**

    This dataset is created by the CSSE at John Hopkins University by gathering information released by official state outlet channels. It contains key fields like update date, country/region, confirmed cases number and death cases number of COVID-19 on a daily basis. 
2. **yfinance**

    yfinance is an open-source tool that uses Yahoo's publicly available API to collect data from Yahoo's finance sector. yfinance will be used to generate historical data for trading stocks. Fields like data, openning price, closing price, high price, low price of the interested stocks will be available. 



## Timeline
**Week 1: Group Work**
- Discuss and finalize the research question to ensure it is clear, relevant, and feasible for the project timeline.
- Search for and evaluate potential datasets that can support the research question, focusing on data reliability, accessibility, and relevance to the topic.
- Decide which datasets will be used and assign initial responsibilities among group members.

**Week 2: Yuhan**
- Perform data cleaning and integrate the selected datasets into a usable format for analysis.
- Discuss potential ethical concerns related to the data, such as privacy, bias, or limitations in representation.
- Check the overall data quality, including missing values, inconsistencies, and formatting issues.

**Week 3: Bowen**
- Conduct data analysis based on the research topic and prepared datasets.
- Create visualizations to present patterns, trends, and relationships identified in the analysis.

**Week 4: Group**
- Interpret and describe the main findings from the analysis.
- Discuss challenges encountered and suggest possible directions for future work.
- Compile and organize all citations and references used in the project.

## Constraints 

The datasets we found are Covid-19's impact on population of different countries and stock price changes of major health firms. The constraints of the Covid-19 data is the difficulty of combining the datasets. This is because that it is a collection of daily record of population, and therefore we would need to combine all the different datasets of our desired timeframe. In addition, since we are only interested in United States, there will be some data filtering work needs to be done and we have to make sure that all United States data are kept, including those that are expressed as "US / U.S. / united states", etc. Also, although we are able to view the stock price data online and retrieve it using an open source library called "yFinance", we are not able to retrieve the raw dataframe using a free account. Therefore, we will only be able to clean and view the data using data analysis technique. 

## Gaps
A limitation of this project is that the COVID-19 data used is aggregated at the country level rather than focusing on specific regions within the United States. Because of this, the analysis may produce conclusions that are relatively broad and may not accurately reflect regional differences such as variations in public health policies, population density, healthcare capacity, or vaccination rates. These regional factors can significantly influence both the spread of COVID-19 and its economic impact, meaning that important localized dynamics may be overlooked in the findings.

Another gap in the research is related to the nature of the datasets themselves. The COVID-19 dataset and the healthcare firm stock price dataset each provide a relatively narrow perspective on their respective domains. As a result, the analysis may identify correlations between pandemic trends and healthcare company stock performance, but these relationships may not necessarily imply causation. Other external variables—such as government stimulus policies, market sentiment, or broader economic conditions—may also influence stock prices and are not fully captured within the datasets used.



