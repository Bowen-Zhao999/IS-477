# Status Report


## Update on tasks

1. We uploaded the necessary artifact, i.e. the John Hopkins Covid-19 data file to Github so that the professor and TAs could make easier access to our dataset. The yfinance dataset we used is not uploaded because it is a Python library that could be downloaded through the terminal easily. If necessary, we could include a installation guide of yfinance in future reports. 

## Update on timeline

1. The combination of multiple CSV files of COVID data from different dates has been completed. The path of the data folder was first obtained through the os library so that we can achieve the automated retrieval of the folder path. Others could replicate this process without the need to manually type in the address of the folder as long as they place the JupyterNotebook in the same directory of the data folder. Afterwards, data from 2021 was selected, and all the 2021 everyday data was integrated as a whole dataframe for further study.

2. The data profiling process has been completed. We noticed that dataset contains a selection of features, however, it would be more efficient for us to use features selectively in later on analysis. The dataset contains complete data for confirmed cases and death cases for COVID, however, there was a large void area in recovered cases and active cases. As a result, we may be forced to rely on confirmed and death numbers solely to engineer our severity index of COVID. The dataset also provided data for all 365 days. 

3. The cleaning process of the dataset has been completed. Based on prior profiling results, we remained four features and eliminated others for our project. We then transformed to date from a string to a date time type, calculated the daily new confirmed and death cases for each region, and finally grouped the regional dataset into a national dataset that reflects new confirmed and death cases on every day.

4. The financial market data retrieval process has been completed. We utilized the yfinance library to automatically download daily stock data for selected healthcare companies, including CVS, JNJ, and ABBV, within the year of 2021. To ensure consistency with the COVID dataset, we resampled the stock data to a daily frequency. Missing values in closing prices were forward-filled to maintain continuity, while trading volume gaps were filled with zeros to reflect non-trading days. Finally, only relevant features (closing price and volume) were retained for further integration.

5. The stock datasets were standardized and reformatted for merging. A helper function was implemented to create uniform column naming conventions across different tickers, allowing each dataset to contain a shared "Date" column along with uniquely identified feature columns (e.g., CVS_Close, JNJ_Volume). Additionally, all date fields were explicitly converted into string format to ensure compatibility during the merging process. This step guarantees that all datasets follow a consistent structure before integration.

6. The dataset integration process has been completed. We sequentially merged the processed stock datasets with the COVID national dataset using left joins on the "Date" column. This approach preserves the full timeline of COVID data while appending corresponding financial indicators for each day. The final combined dataframe contains synchronized daily records of pandemic severity metrics and stock market performance, forming a unified dataset for subsequent analysis.

## Changes on plan based on feedback

1. During this phase of the project, we successfully transitioned from raw data collection to a structured, integrated dataset by reconciling the disparate timelines of public health and financial records. A significant pivot in our plan involved narrowing the COVID-19 severity metrics; upon discovering substantial missing values for "Recovered" and "Active" cases during the data profiling stage, we have refine our analysis to focus exclusively on confirmed cases and mortality rates to ensure statistical integrity. 

2. Furthermore, we addressed feedback regarding project reproducibility by implementing automated directory pathing via the os library and providing explicit documentation for our data sources. By standardizing the yfinance healthcare stock data (CVS, JNJ, ABBV) with forward-filled prices to account for non-trading days, we have established a synchronized daily dataframe that serves as a robust foundation for examining the correlation between pandemic surges and market volatility in 2021.

## Challenges and problems met so far

1. A primary challenge we encountered was the initial "noise" within our raw data. The source dataset was massive, containing over 1,000 subsets that encompassed three full years of COVID-19 mortality and diagnosis information. However, for the specific scope of our study, we required only a single year of data. To solve this, we moved away from manual spreadsheet filtering—which proved both slow and prone to oversight and implemented a programmatic filtering strategy using the Python Pandas library. By defining specific date range parameters and utilizing boolean indexing, we were able to systematically truncate the dataset. This shift was critical; it allowed us to isolate the necessary 12-month period with 100% accuracy, effectively transforming a fragmented 1,000 subset archive into a streamlined, analysis-ready master file.

2. Once the relevant data was isolated, the next challenge was integration. Because the data was spread across numerous sub-datasets, we faced "schema drift"—where different files had slightly different column headers or formatting. Merging these into a single, cohesive master file required ensuring that every record aligned perfectly by date and region. We addressed this by performing a data join in Python. We standardized the column names across all subsets and used the pd.merge() functions to unify the disparate files. 

3. To add a layer of economic context to our COVID-19 analysis, we needed reliable stock market data. Initially, we struggled to find a way to import high-fidelity financial records without manually downloading dozens of CSV files, which would have been prone to human error and difficult to update. After researching automated data retrieval methods, we discovered and implemented the yfinance library in Python. This library provides a direct threaded interface to the Yahoo Finance API. By using the yf.download() method, we were able to pull real-time historical data directly into our workspace.

## Short summary of contribution for each member

- Bowen Zhao: 
    - Revisited and refined the project plan. 
    - Managed the Github repository and the upload of deliverables and artifacts. 
    - Constructed a dynamic path resolution, performed data integration and cleaning on the COVID dataset, and aggregated regional-level data into a unified national-level dataframe for analysis.

- Yuhan Zhou
    - Revisited and refined the project plan along side with teammates. 
    - Perfromed data cleaning and integration of the yFinance dataset, and joined the datasets of both COVID and yFinance. 