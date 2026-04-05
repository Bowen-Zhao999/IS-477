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

## Challenges and problems met so far

## Short summary of contribution for each member

- Bowen Zhao: 
    - Revisited and refined the project plan. 
    - Managed the Github repository and the upload of deliverables and artifacts. 
    - Constructed a dynamic path resolution, performed data integration and cleaning on the COVID dataset, and aggregated regional-level data into a unified national-level dataframe for analysis.

- Yuhan Zhou
    - 