## Title: COVID-19 and Health Firm Stock Price


## Contributors: 
- Bowen Zhao
- Yuhan Zhou


## Summary: [500-600 words] Description of your project, motivation, research question(s), and any findings.

In this project, we explored the relationship between a global health catastrophe, COVID-19, and the resilience of capital markets. Specifically, we investigate how the severity of the COVID-19 pandemic—measured through infection and mortality rates—influenced the financial performance of the United States health sector during the critical window between January 1, 2021, to January 1, 2022. This period is particularly significant as it included the period of the vaccines, the emergence of the Delta and Omicron variants, and a shift in market sentiment from panic to strategic long-term valuation of healthcare equities.

The motivation behind this study stems from the nature of the COVID outbreak. Unlike traditional economic shocks driven by housing or credit bubbles, this was a biological catalyst that restructured global priorities fundamentally. For the healthcare and pharmaceutical industry, the pandemic presented a reality that a moral obligation to innovate and a massive commercial opportunity. We wanted to quantify this impact. As the threat of the virus grew more dreadful in the eyes of the public, we want to discover in the project that whether the stock market respond in a linear fashion to the rising death counts, or did it anticipate medical breakthroughs before they reflected in health statistics.

Therefore, our research centralizes on the question: What is the statistical and predictive relationship between U.S. COVID-19 case/death counts and the stock price fluctuations of major pharmaceutical firms during 2021?

**Methodology and Technical Execution**
In order to answer this, our team developed a analytical pipeline designed to merge different data streams. We utilized the Johns Hopkins University COVID-19 Repository for high-resolution health data and the yfinance API to extract historical financial time-series data (including Open, High, Low, and Closing prices).

The execution required some data engineering. To acheive this, we employed SQL for relational mapping and Python’s Pandas library for initial data cleaning. A primary challenge evolved in data cleaning and normalization, which we had to standardize namings of the daily records and align the seven-day-a-week health data with the five-day-a-week trading schedule of the New York Stock Exchange. In addition to simple correlation, we implemented machine learning models via scikit-learn to identify the sensitivity of these stocks, thereby attempt to see if pandemic-driven news cycles could serve as a leading indicator for stock volatility.

**Findings and Gaps**
- PLACEHOLDER FOR UNFINISHED FINDING PART!!!
> *Our analysis revealed a nuanced correlation. While a general upward trend in pharmaceutical valuation mirrored the periods of increased case counts, the market often displayed a more forward-looking behavior. While stock prices frequently surged in anticipation of FDA approvals or trial results, sometimes decoupled from the immediate daily death rates. This observation from the data suggested that while health crises drive sector interest, market sentiment is more sensitive to solutions such as vaccines, than to the problems like infection themselves.*

However, the study has some constraints. The reliance on country-level aggregated data created a regional gap, which obscured how localized policy between states shifts or vaccination rates in specific states could have influenced broader market trends. In addition, we identified a gap that, while correlations exist, they are influenced by latent variables such as government stimulus packages and broader shifts in interest rates.

Ultimately, this project highlights that during a global health crisis, the pharmaceutical sector functions as a highly speculative asset class. The results underscore the necessity for investors and policymakers to look beyond raw health statistics and consider the broader socio-economic ecosystem when predicting market behavior in times of biological volatility.



## ata profile: [max2000 words] For each dataset used, describe its structure, content, and characteristics. Specify the location of the dataset files in your project repository. Discuss any ethical or legal constraints associated with the data and explain how the datasets relate to your questions

**COVID-19 Data Repository (JHU CSSE)**
The data is sourced from the Johns Hopkins University Center for Systems Science and Engineering (CSSE). It consists of daily CSV reports of the pandemic's status globally and within the U.S.
- Format: Daily CSV files (Relational mapping via Date).  
- Key Variables:
Geographic Identifiers: Province_State, Country_Region, Lat, Long_, FIPS (unique US county codes), UID, ISO3.

Public Health Metrics: Confirmed (total cases), Deaths (total fatalities), Recovered, and Active (calculated as Confirmed - Deaths - Recovered).

Analytical Rates: Incident_Rate (cases per 100k), Case_Fatality_Ratio (percentage of confirmed cases resulting in death), and Mortality_Rate.

Infrastructure Data: Total_Test_Results, People_Hospitalized, Testing_Rate.

- Characteristics: This is time-series aggregate data. Since our project focuses on the U.S., we filter for Country_Region == 'US'. The data is cumulative, requiring us to calculate "Daily New Cases" by subtracting $Day_{n}$ from $Day_{n-1}$.

**Pharmaceutical Stock Market Dataset (yfinance)**
This dataset was generated using the yfinance library, which interfaces with Yahoo Finance to pull historical market data for three specific tickers: CVS (CVS Health), JNJ (Johnson & Johnson), and ABBV (AbbVie).
- Format: Tabular time-series data (Pandas DataFrame).
- Variables:
Date: The primary key for merging with COVID-19 data.

Close: The closing price of the stock on a given day (our primary dependent variable).

Volume: The total number of shares traded (used to measure market "excitement" or volatility).

Additional Fields: While we focused on Close and Volume, the raw data also includes Open, High, Low, and Adj Close.

- Characteristics: Unlike the COVID-19 data (which is 7 days a week), stock data follows the business calendar. There is no data for weekends or federal holidays. To bridge this gap, we used "forward-filling" or "rolling averages" in our pipeline.

**Ethical or Legal Constraints**
For the JHU CSSE dataset, it is provided in aggregate form, meaning it contains no Personally Identifiable Information (PII). This circumvents HIPAA concerns, as individual patients cannot be identified. However, ethical care is required when interpreting data from marginalized communities where reporting may have been less accurate. Its licencing is provided under a Creative Commons Attribution 4.0 International (CC BY 4.0) license. It is free for educational and research use, provided that proper credit is given to the JHU CSSE.

For the Pharmaceutical stock market dataset, it is public information. Therefore, the primary ethical concern is the risk of misinformation if we were to present correlation as definitive financial advice. Our project explicitly states it is for retrospective research, not predictive trading. Its licencing is from yfinance, which is an open-source tool that scrapes public Yahoo Finance pages. Although Yahoo Finance's Terms of Service generally prohibit high-frequency commercial scraping, our use case involves a one-time retrieval of historical data for non-commercial research, which generally falls under its Fair Use.



## Data quality: [500-1000 words] Summary of the quality assessment.

For this project, we assessed the quality of the Johns Hopkins University (JHU) COVID-19 dataset and the yfinance pharmaceutical dataset based on completeness, consistency, and reliability.

1. Financial Data Integrity (yfinance)
The stock market data for CVS, JNJ, and ABBV was relatively robust. Upon data extraction and auditing, we observed that there is zero missing values for the primary variables of interest: Date, Close, and Volume.

We believe this high level of completeness is gely due to the regulated nature of financial reporting. Since we are targeting three major firms on the New York Stock Exchange, the price feeds are continuous and authoritative. The only gap in the timeline were the expected absences of data on weekends and federal holidays. Rather than treating these as missing data points, we recognized them as a structural characteristic of capital markets. To maintain synchronization with the daily health data, we implemented a forward-fill methodology, where the stock price on a Saturday or Sunday is assumed to be the closing price of the preceding Friday.

2. Public Health Data Quality (JHU CSSE)
The JHU COVID-19 dataset is a secondary aggregate, meaning its quality is dependent on the reporting accuracy of individual U.S. states and counties. Our assessment revealed the following:

Handling of Null Values
Our initial audit found 58 null values in the New_Confirmed and New_Deaths columns. Interestingly, all 58 instances occurred on January 1, 2021. Therefore, we think that this is not a failure of data collection, but because of the dataset's structure. Since January 1st marks the start of our specific observation window and the "new" cases are calculated as a delta from the previous day's cumulative total, the absence of a "Day 0" (December 31, 2020) in our specific filtered subset resulted in these initial nulls.

To resolve this without skewing the results, we cross-referenced the cumulative totals from the final day of 2020 to populate these starting values, ensuring that our time-series analysis began with a verified baseline.

3. Cross-Dataset Synchronization
The most significant challenge was the relational mapping between the two datasets. We performed a join operation on the Date variable, but because the health data is provided at a county/state level and the stock data is national, we had to aggregate the JHU data into a single national daily total.

We verified the success of this aggregation by comparing our calculated national daily sums against official CDC (Centers for Disease Control and Prevention) reports. 

4. Final Quality Verdict
Overall, the datasets are of high quality and high fidelity. The yfinance data provides a clean reflection of market sentiment, while the JHU data—despite the initial null values on January 1st and the inherent noise of public health reporting—remains the gold standard for pandemic tracking. In conclusion, we have established a data foundation that is both statistically sound and technically reliable for investigating the intersection of public health and finance.



## Data cleaning: [max 1000 words] Summarize the data cleaning operations you performed and explain how each operation addressed specific data quality issues in your datasets.



## Findings: [~500 words] Description of any findings including numeric results and/or visualizations.



## Future work: [~500-1000 words] Brief discussion of any lessons learned and potential future work.



## Challenges: [~500 words] Discuss the main challenges you encountered while working on the project.



## Reproducing: Sequence of steps required for someone else to reproduce your results.



## References: Formatted citations for any papers, datasets, or software used in your project.



