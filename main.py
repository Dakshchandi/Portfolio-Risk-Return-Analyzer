import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def annual_return(starting, ending, period):
    ret = ((ending / starting) ** (1 / period)) - 1
    return ret * 100


def annual_volatility(closing):
    daily_return = closing.pct_change()
    daily_standard_dev = daily_return.std()
    annual_vol = daily_standard_dev * np.sqrt(252)
    return annual_vol * 100


def sharpe_ratio(annual_return, annual_volatility, risk_free_rate):
    return (annual_return - risk_free_rate) / annual_volatility


def max_drawdown(closing):
    running_max = closing.cummax()
    drawdown = (closing - running_max) / running_max
    return drawdown.min() * 100


def portfolio_annual_return(annual_ret_of_stocks, weights):
    total = 0
    for i in range(stocks_number):
        total += annual_ret_of_stocks[i] * weights[i]
    return total / 100


def downside_volatility(daily_returns, risk_free_rate_annual=0):
    # convert annual risk-free rate (%) to daily decimal rate
    daily_rf = (risk_free_rate_annual / 100) / 252

    # keep only returns below the daily risk-free threshold
    downside_returns = daily_returns[daily_returns < daily_rf] - daily_rf

    if len(downside_returns) == 0:
        return 0

    downside_std = downside_returns.std()
    annual_downside_vol = downside_std * np.sqrt(252)
    return annual_downside_vol * 100


def sortino_ratio(annual_return, downside_volatility, risk_free_rate):
    if downside_volatility == 0:
        return np.nan
    return (annual_return - risk_free_rate) / downside_volatility


tickter = []
weights = []
annual_ret_of_stocks = []

stocks_number = int(input("Enter the number of Stocks You Have : "))

for i in range(stocks_number):
    stock = input(f"Enter Your {i+1} stock TICKETER SYMBOL : ").upper()
    weight_stock = float(input(f"Enter Your {i+1} stock weight (eg. 25% = 25) : "))
    tickter.append(stock)
    weights.append(weight_stock)

months = int(input("Enter the time peroid in months : "))
risk_free_rate = float(input("Enter your Risk free rate : "))
period = f"{months}mo"
period_in_yrs = months / 12

total_weight = sum(weights)

if abs(total_weight - 100) >0.1:
    raise ValueError("Portfolio weights must sum to 100.")


# =========================
# Comparator choice
# =========================
comparitors = {
    "Nifty 50": "^NSEI",
    "S&P500": "^GSPC",
    "Banknifty": "^NSEBANK",
    "SENSEX": "^BSESN",
    "Nasdaq-100": "^NDX",
    "DAX 40": "^GDAXI",
    "FTSE 100": "^FTSE",
    "EURO STOXX 50": "^STOXX50E"
}

comparitor_names = list(comparitors.keys())

print("Choose a comparator index:")
for i, name in enumerate(comparitor_names, start=1):
    print(f"{i}. {name}")

choice = int(input("Enter your choice number: "))
if choice < 1 or choice > len(comparitor_names):
    raise ValueError("Invalid comparator choice.")

comparitor_name = comparitor_names[choice - 1]
comparitor_ticker = comparitors[comparitor_name]

print(f"You selected: {comparitor_name} ({comparitor_ticker})")

# download comparator data
comparitor_data = yf.download(comparitor_ticker, period=period)
if comparitor_data.columns.nlevels > 1:
    comparitor_data.columns = comparitor_data.columns.droplevel(1)

comparitor_daily_return = comparitor_data["Close"].pct_change().dropna()
comparitor_cumulative = (1 + comparitor_daily_return).cumprod() - 1


# =========================
# Stock-level analysis
# =========================
stock_daily_returns = pd.DataFrame()
stock_cumulative_returns = pd.DataFrame()

for ticket in tickter:
    data = yf.download(ticket, period=period)

    daily_return = data[("Close", ticket)].pct_change().dropna()
    stock_daily_returns[ticket] = daily_return

    start_price = data[("Open", ticket)].iloc[0]
    end_price = data[("Close", ticket)].iloc[-1]

    annual_ret = annual_return(start_price, end_price, period_in_yrs)
    close_prices = data[("Close", ticket)]
    annual_volit = annual_volatility(close_prices)
    shrape_ratioo = sharpe_ratio(annual_ret, annual_volit, risk_free_rate=0)

    stock_downside_vol = downside_volatility(daily_return, risk_free_rate_annual=0)
    stock_sortino = sortino_ratio(annual_ret, stock_downside_vol, 0)

    max_drawdownn = max_drawdown(close_prices)

    annual_ret_of_stocks.append(annual_ret)

    cumulative_return = (1 + daily_return).cumprod() - 1
    stock_cumulative_returns[ticket] = cumulative_return

    print(f"Annula return for {ticket} is : {annual_ret:.2f}%")
    print(f"Annula volatility for {ticket} is : {annual_volit:.2f}%")
    print(f"Shrape Ratio for {ticket} is : {shrape_ratioo:.2f}")
    print(f"Sortino Ratio for {ticket} is : {stock_sortino:.2f}")
    print(f"Max Drawdown for {ticket} is : {max_drawdownn:.2f}%")

print("---------------------------------------------------")
print("Summary of your Portfolio : ")
print("---------------------------------------------------")


# =========================
# Portfolio calculations
# =========================

# portfolio annual return
portfolio_return = portfolio_annual_return(annual_ret_of_stocks, weights)

# portfolio daily return series
portfolio_daily_return = 0
for i, ticker in enumerate(tickter):
    data = yf.download(ticker, period=period)
    if data.columns.nlevels > 1:
        data.columns = data.columns.droplevel(1)

    daily_return = data["Close"].pct_change().dropna()
    portfolio_daily_return += (weights[i] / 100) * daily_return

# export portfolio daily returns
portfolio_daily_return_df = (portfolio_daily_return * 100).to_frame(name="Portfolio Daily Return (%)")
portfolio_daily_return_df.to_excel("portfolio_daily_return.xlsx")

# portfolio volatility
portfolio_volatility = (portfolio_daily_return.std() * np.sqrt(252)) * 100

# portfolio Sharpe ratio
portfolio_sharpe_ratio = sharpe_ratio(portfolio_return, portfolio_volatility, risk_free_rate)

# portfolio Sortino ratio
portfolio_downside_volatility = downside_volatility(portfolio_daily_return, risk_free_rate)
portfolio_sortino_ratio = sortino_ratio(portfolio_return, portfolio_downside_volatility, risk_free_rate)

# portfolio max drawdown
portfolio_cumulative_for_drawdown = (1 + portfolio_daily_return).cumprod()
portfolio_running_max = portfolio_cumulative_for_drawdown.cummax()
portfolio_drawdown = (portfolio_cumulative_for_drawdown - portfolio_running_max) / portfolio_running_max
portfolio_max_drawdown = portfolio_drawdown.min() * 100

# cumulative return of portfolio
portfolio_cumulative = (1 + portfolio_daily_return).cumprod() - 1

# align portfolio with comparator
comparison_df = pd.concat(
    [
        portfolio_cumulative.rename("Portfolio"),
        comparitor_cumulative.rename(comparitor_name)
    ],
    axis=1
).dropna()

# 30-day rolling volatility
rolling_volatility = (portfolio_daily_return.rolling(30).std() * np.sqrt(252)) * 100

# 30-day rolling Sharpe ratio
rolling_mean = portfolio_daily_return.rolling(30).mean()
rolling_vol = portfolio_daily_return.rolling(30).std()
rolling_annual_return = rolling_mean * 252
rolling_annual_vol = rolling_vol * np.sqrt(252)
rolling_sharpe = rolling_annual_return / rolling_annual_vol


print("Portfolio daily return exported to portfolio_daily_return.xlsx")
print(f"Annual return for your portfolio : {portfolio_return:.2f}%")
print(f"Annual volatility of your portfolio : {portfolio_volatility:.2f}%")
print(f"Shrape ratio of your portfolio : {portfolio_sharpe_ratio:.2f}")
print(f"Portfolio Sortino Ratio : {portfolio_sortino_ratio:.2f}")
print(f"Portfolio Max Drawdown is : {portfolio_max_drawdown:.2f}%")


# =========================
# PLOTS
# =========================

# plot for portfolio vs comparator cumulative return
plt.figure(figsize=(12, 6))
plt.plot(comparison_df.index, comparison_df["Portfolio"] * 100, label="Portfolio")
plt.plot(comparison_df.index, comparison_df[comparitor_name] * 100, label=comparitor_name)
plt.title(f"Portfolio vs {comparitor_name} Cumulative Return")
plt.xlabel("Date")
plt.ylabel("Cumulative Return (%)")
plt.legend()
plt.grid(True)
plt.show()

# plot for cumulative return of each stock
plt.figure(figsize=(12, 6))
for col in stock_cumulative_returns.columns:
    plt.plot(stock_cumulative_returns.index, stock_cumulative_returns[col] * 100, label=col)

plt.title("Cumulative Return of Each Stock")
plt.xlabel("Date")
plt.ylabel("Cumulative Return (%)")
plt.legend()
plt.grid(True)
plt.show()

# plot for rolling 30-day Sharpe ratio
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe.index, rolling_sharpe, label="30-Day Rolling Sharpe Ratio")
plt.title("Portfolio 30-Day Rolling Sharpe Ratio")
plt.xlabel("Date")
plt.ylabel("Sharpe Ratio")
plt.legend()
plt.grid(True)
plt.show()

# plot for rolling 30-day volatility
plt.figure(figsize=(12, 6))
plt.plot(rolling_volatility.index, rolling_volatility, label="30-Day Rolling Volatility")
plt.title("Portfolio 30-Day Rolling Volatility")
plt.xlabel("Date")
plt.ylabel("Volatility (%)")
plt.legend()
plt.grid(True)
plt.show()


print(period_in_yrs)
print(tickter)
print(weights)

