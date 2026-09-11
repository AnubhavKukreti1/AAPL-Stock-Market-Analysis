🍎 Apple Inc. (AAPL) Stock Market Analysis

Interactive Exploratory Data Analysis Dashboard for Apple Inc. (AAPL)

An interactive stock market analysis dashboard built with Python, Streamlit, Pandas, NumPy, Plotly, and yfinance.

The project analyzes historical Apple stock data to explore price trends, returns, volatility, trading activity, drawdowns, moving averages, monthly performance, and performance relative to the S&P 500.

📊 Project Overview

This project combines exploratory data analysis with an interactive Streamlit dashboard to provide a comprehensive view of Apple's historical stock performance.

Users can select different historical periods and interactively explore AAPL market data through charts, performance metrics, risk indicators, and benchmark comparisons.

Dashboard Includes
📈 Historical AAPL price analysis
📊 50-day and 200-day moving averages
🕯️ Candlestick analysis
💰 Daily return analysis
📉 Daily return distribution
⚠️ Volatility and risk analysis
📉 Maximum drawdown analysis
📊 Trading volume analysis
📅 Monthly return heatmap
📆 Annual return analysis
🆚 AAPL vs S&P 500 performance
🔗 AAPL vs S&P 500 return correlation
📊 Trading volume vs daily returns
📥 Historical data download as CSV
🎛️ Interactive historical-period selection
🚀 Interactive Dashboard

The dashboard provides multiple analytical sections:

Section	Description
📊 Overview	Project summary, key findings, and visualizations
📈 Price	Historical price, moving averages, and candlestick chart
💰 Returns	Daily returns, distribution, statistics, and monthly performance
⚠️ Risk	Volatility, Sharpe ratio, drawdown, and trading activity
🆚 Benchmark	AAPL performance compared with the S&P 500
🗃️ Data	Historical market data with CSV download
📌 Key Performance Metrics

The dashboard calculates several important financial metrics:

Total Return

Measures the overall percentage change in AAPL's price over the selected period.

Annualized Return

Estimates the average yearly return over the selected period.

Annualized Volatility

Measures the variability of daily returns and is annualized using 252 trading days.

Sharpe Ratio

A simplified Sharpe ratio is calculated using a 0% risk-free rate for educational purposes.

Maximum Drawdown

Measures the largest decline from a previous peak in the stock price.

Positive / Negative Trading Days

Shows the percentage of trading days with positive and negative returns.

Trading Volume

Analyzes average trading activity and volume patterns.

📈 Visualizations

The project contains a collection of pre-generated analytical visualizations stored in the visualization/ directory.

Price & Trend Analysis
AAPL adjusted closing price
AAPL price with moving averages
Historical price trends
Return Analysis
Daily return distribution
Monthly returns heatmap
Annual returns
Risk Analysis
Historical drawdown
30-day rolling annualized volatility
Benchmark & Relationship Analysis
AAPL vs S&P 500 cumulative performance
AAPL vs S&P 500 return correlation
Trading volume vs daily returns
🛠️ Tech Stack
Technology	Purpose
🐍 Python	Core programming language
🐼 Pandas	Data manipulation and analysis
🔢 NumPy	Numerical calculations
📊 Plotly	Interactive visualizations
🎈 Streamlit	Interactive dashboard
📈 yfinance	Yahoo Finance market data
📓 Jupyter Notebook	Exploratory data analysis
📂 Project Structure
Stock-Market-Analysis/
│
├── app.py
│
├── requirements.txt
│
├── data/
│
├── notebooks/
│   └── Analysis.ipynb
│
├── visualization/
│   ├── AAPL_adjusted_closing_price.png
│   ├── AAPL_price_moving_averages.png
│   ├── AAPL_daily_returns_distribution.png
│   ├── AAPL_trading_volume.png
│   ├── AAPL_historical_drawdown.png
│   ├── AAPL_vs_SP500_cumulative_performance.png
│   ├── AAPL_monthly_returns_heatmap.png
│   ├── AAPL_annual_returns.png
│   ├── AAPL_30day_rolling_annualized_volatility.png
│   ├── AAPL_SP500_return_correlation.png
│   └── AAPL_volume_vs_daily_returns.png
│
└── README.md

⚙️ Installation
1. Clone the Repository
git clone <your-repository-url>
cd Stock-Market-Analysis

2. Create a Virtual Environment
python -m venv venv


Activate it on macOS/Linux:

source venv/bin/activate


On Windows:

venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

▶️ Run the Dashboard

Start the Streamlit application:

streamlit run app.py


The dashboard will open in your browser.

📊 Data Source

Market data is retrieved using the yfinance Python library, which provides access to historical financial market data from Yahoo Finance.

The dashboard dynamically downloads:

AAPL historical market data
S&P 500 (^GSPC) benchmark data

The application supports multiple historical periods:

1 Year
2 Years
5 Years
10 Years
Maximum available history
🔍 Exploratory Analysis

The underlying analysis investigates several aspects of AAPL's historical behavior.

Price Trends

Moving averages are used to identify short-term and long-term price trends.

Return Behavior

Daily percentage returns are analyzed to understand the distribution and variability of stock performance.

Risk

Volatility, drawdowns, and the Sharpe ratio provide different perspectives on historical risk.

Trading Activity

Trading volume is analyzed alongside price movements and daily returns.

Benchmark Comparison

AAPL is compared against the S&P 500 to evaluate relative performance over the same period.

💡 Example Questions This Dashboard Can Answer

The dashboard can be used to explore questions such as:

How has AAPL performed over the last 5 years?
What has been Apple's annualized return?
How volatile has AAPL been?
What was Apple's largest historical drawdown?
How frequently did AAPL have positive trading days?
How does AAPL compare with the S&P 500?
What does the daily return distribution look like?
Are periods of high trading volume associated with large returns?
How have monthly returns changed over time?
How does AAPL's performance vary across different market periods?
🎯 Project Goals

The main objectives of this project are to:

Practice financial data analysis using Python.
Perform exploratory data analysis on real-world market data.
Develop meaningful financial performance metrics.
Create clear and interactive data visualizations.
Compare individual stock performance against a market benchmark.
Build and deploy an interactive Streamlit dashboard.
Present analytical findings in a professional data-science portfolio project.
📈 Future Improvements

Potential extensions to the project include:

📊 Additional technical indicators such as RSI and MACD
📉 Bollinger Bands
📈 Exponential Moving Averages
🔗 Rolling correlation analysis
🧮 Beta calculation against the S&P 500
📐 Value at Risk (VaR)
📊 Portfolio analysis
🤖 Basic return prediction models
📰 Sentiment analysis using financial news
☁️ Cloud deployment
📱 Improved mobile dashboard layout
⚠️ Disclaimer

This project is intended for educational and analytical purposes only.

The analysis is based on historical market data. Historical performance does not guarantee future results.

Nothing in this project should be considered financial, investment, or trading advice.

👨‍💻 Project

Apple Inc. (AAPL) Stock Market Analysis

Built using:

Python • Pandas • NumPy • Plotly • Streamlit • yfinance

⭐ If you find this project useful, consider giving the repository a star!
