# forex-feature-engineering

## Forex Trading Strategy Search
This project aims to develop and evaluate trading strategies based on technical indicators to predict the next day's price direction. Instead of blindly trusting popular strategies, we systematically test thousands of indicator combinations to find statistically significant trading conditions.

## Overview
The project consists of the following steps:

### Part 1 
TechInd_strategy_backtester.ipynb
Project Goals
- Collect real trading data (e.g., from OANDA).
- Backtest trading strategies that use combinations of technical indicators.
- Optimize indicator parameters for statistically reliable buy/sell conditions.
- Test strategies across multiple time periods to avoid overfitting.
- Use Bayesian optimization to find robust parameter sets.
- Evaluate results using confidence intervals to ensure realistic expectations.

### How It Works
- Generate Trading Strategies. Combine different technical indicators (e.g., RSI, SMA, Stochastics).
Create thousands of potential buy/sell conditions.
Backtest Strategies

- Simulate trades using historical data. Calculate final return, max return, and min return for each strategy.
Consider trading commissions and realistic stop-loss/take-profit levels.

- Analyze Performance. Identify the best-performing strategies based on return metrics.

- Test performance consistency across multiple time periods.

- Evaluate the distribution of returns to detect overfitting.

- Find Statistically Reliable Strategies. Or Not! 

- Apply Bayesian optimization to tune indicator parameters.
- Select strategies with positive mean return within confidence intervals.

### Part 2 
FinNews_feature_extract.ipynb
- **Reuters news archive scraper**
- **News sensitivity analysis and relevant information extraction**
- **LSTM NN regression model**: 3 day ahead prices prediction obased on recent prices and news.
- **LSTM NN Performance Evaluating**  


## Acknowledgments
Special thanks to the developers of the TA-Lib library, which was used extensively in the generation of technical indicators and ChatGPT. 
