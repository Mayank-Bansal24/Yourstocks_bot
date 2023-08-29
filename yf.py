import yfinance as yf

# Replace with the stock symbol you want to fetch (e.g., TCS.BO for Tata Consultancy Services on BSE)
stock_symbol = "INFY.BO"

# Fetch stock data
stock_data = yf.Ticker(stock_symbol)

# Get the most recent price
current_price = stock_data.history(period='1d')['Close'][-1]

print(f"Current price of {stock_symbol}: {current_price:.2f}")
