# Portfolio-Risk-Return-Analyzer

A Python-based portfolio analytics tool that uses **Yahoo Finance market data** to evaluate the performance and risk profile of individual stocks and multi-asset portfolios. The project calculates key return and risk metrics such as **annual return, annual volatility, Sharpe ratio, Sortino ratio, and maximum drawdown**, while also comparing portfolio performance against a benchmark index with **cumulative return and rolling risk visualizations**.

---

## Features

### Stock-level analytics

For each stock in the portfolio, the tool calculates:

* **Annual Return**
* **Annual Volatility**
* **Sharpe Ratio**
* **Sortino Ratio**
* **Maximum Drawdown**
* **Cumulative Return Series**

### Portfolio-level analytics

For the portfolio as a whole, the tool calculates:

* **Portfolio Annual Return**
* **Portfolio Annual Volatility**
* **Portfolio Sharpe Ratio**
* **Portfolio Sortino Ratio**
* **Portfolio Maximum Drawdown**
* **Portfolio Daily Return Export to Excel**
* **Rolling 30-Day Volatility**
* **Rolling 30-Day Sharpe Ratio**

### Benchmark comparison

The portfolio can be compared against a benchmark index selected by the user. Supported comparators include:

* Nifty 50
* S&P 500
* Bank Nifty
* Sensex
* Nasdaq-100
* DAX 40
* FTSE 100
* EURO STOXX 50

### Visualizations

The script generates the following plots:

* **Portfolio vs Benchmark Cumulative Return**
* **Cumulative Return of Each Stock**
* **30-Day Rolling Sharpe Ratio**
* **30-Day Rolling Volatility**

---

## Tech Stack

* **Python**
* **yfinance** – for downloading market data from Yahoo Finance
* **pandas** – for time series handling and portfolio calculations
* **NumPy** – for numerical operations
* **Matplotlib** – for plotting and visualization

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/Portfolio-Risk-Return-Analyzer.git
cd Portfolio-Risk-Return-Analyzer
```

Install the required dependencies:

```bash
pip install yfinance pandas numpy matplotlib openpyxl
```

---

## How It Works

The script takes user input for:

1. **Number of stocks in the portfolio**
2. **Ticker symbol of each stock**
3. **Weight of each stock in the portfolio**
4. **Investment time period (in months)**
5. **Risk-free rate**
6. **Benchmark comparator index**

Using this information, it downloads historical price data from Yahoo Finance and performs both **stock-level** and **portfolio-level** return and risk analysis.

---

## Example Workflow

When you run the script, it will ask for portfolio inputs such as:

```text
Enter the number of Stocks You Have : 3
Enter Your 1 stock TICKETER SYMBOL : AAPL
Enter Your 1 stock weight (eg. 25% = 25) : 40
Enter Your 2 stock TICKETER SYMBOL : MSFT
Enter Your 2 stock weight (eg. 25% = 25) : 35
Enter Your 3 stock TICKETER SYMBOL : GOOGL
Enter Your 3 stock weight (eg. 25% = 25) : 25
Enter the time peroid in months : 12
Enter your Risk free rate : 6
Enter your choice number: 2
```

The script then:

* downloads stock and benchmark data
* computes return and risk metrics for each stock
* calculates portfolio metrics
* exports portfolio daily returns to an Excel file
* generates visualizations for performance and risk analysis

---

## Output

### Console output

The script prints stock-level and portfolio-level performance metrics such as:

* Annual return
* Annual volatility
* Sharpe ratio
* Sortino ratio
* Maximum drawdown

### Excel output

The portfolio daily return series is exported as:

```text
portfolio_daily_return.xlsx
```

### Graphical output

The script displays:

* Portfolio vs benchmark cumulative return chart
* Individual stock cumulative return chart
* Rolling Sharpe ratio chart
* Rolling volatility chart

---

## Project Structure

```bash
Portfolio-Risk-Return-Analyzer/
│
├── portfolio_analyzer.py
├── portfolio_daily_return.xlsx   # generated after running the script
└── README.md
```

---

## Metrics Used

### 1. Annual Return

Measures the annualized growth rate of a stock or portfolio over the selected investment period.

### 2. Annual Volatility

Measures the annualized standard deviation of daily returns, representing total risk.

### 3. Sharpe Ratio

Measures risk-adjusted return using total volatility.

**Formula:**

```text
Sharpe Ratio = (Annual Return - Risk-Free Rate) / Annual Volatility
```

### 4. Sortino Ratio

Measures risk-adjusted return using only downside volatility.

**Formula:**

```text
Sortino Ratio = (Annual Return - Risk-Free Rate) / Downside Volatility
```

### 5. Maximum Drawdown

Measures the largest peak-to-trough decline in the value of a stock or portfolio over the selected period.

---

## Example Use Cases

This project can be useful for:

* **Retail investors** analyzing portfolio risk and return
* **Finance students** learning portfolio performance metrics
* **Python learners** building real-world financial analytics projects
* **Anyone comparing a custom portfolio against a benchmark index**

---

## Limitations

* The tool currently uses **interactive console input** rather than a graphical interface.
* Market data depends on **Yahoo Finance availability and ticker accuracy**.
* Portfolio weights must sum to **100%**.
* Some calculations are based on the selected historical period only and do not represent future performance.

---

## Possible Improvements

Future enhancements could include:

* A **Streamlit or Flask dashboard**
* Support for **CSV portfolio uploads**
* Better handling of **invalid tickers and missing data**
* Portfolio return calculation from a unified return series
* Additional ratios such as **Beta, Alpha, Treynor Ratio, and Calmar Ratio**
* Correlation matrix and portfolio optimization features
* Support for **rebalancing simulation**

---

## Contributing

Contributions, improvements, and suggestions are welcome. If you’d like to improve the project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Open a pull request

---

## Disclaimer

This project is for **educational and analytical purposes only** and should not be considered financial advice. Always do your own research before making investment decisions.

---

## License

**MIT License**.
