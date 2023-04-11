# forex-feature-engineering

## Forex Trading Strategy Search
This project aims to identify profitable trading strategies for different Forex pairs and granularities over a given period of time. The project utilizes feature engineering techniques to search for combinations of technical indicators that have a higher potential to predict the correct price swing direction. The generated combinations are then used as features for a Support Vector Machine (SVM) model to boost strategy prediction power.

## Overview
The project consists of the following steps:

### Part 1
- **Data Import**: Import data a given Forex pair, granularity, and time period from OANDA api (some data files used in project are aready saved in hist_data directory).
- **Data Preprocessing**: Convert OANDA jason data to dataframe, clean and preprocess.
- **Feature Generation**: Apply numerous technical indicators to the preprocessed data, generating a large set of potential trading strategies.
- **Labeling**: Calculate the expected profit for each trading strategy, and label each strategy as either "profitable" or "unprofitable".
- **Strategy Search**: Search through the field of all possible trading strategies, selecting only those with a high potential to generate profit.
- **Model Training**: Train a Support Vector Machine (SVM) Classification model using the selected profitable indicator combinations as features.
- **SVM Classification Model Performance Evaluating**

### Part 2
- **Reuters news archive scraper**
- **News sensitivity analysis and relevant information extraction**
- **LSTM NN regression model**: 3 day ahead prices prediction obased on recent prices and news.
- **LSTM NN Performance Evaluating**  


## Acknowledgments
Special thanks to the developers of the TA-Lib library, which was used extensively in the generation of technical indicators and ChatGPT for this marvelous README file. 
