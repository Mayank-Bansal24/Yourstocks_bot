from nsetools import Nse

# Create an instance of the NSE class
nse = Nse()

# Replace 'TCS' with the actual stock symbol you want to fetch
stock_symbol = 'TCS'

# Fetch stock quote
stock_quote = nse.get_quote(stock_symbol)

# Extract the last traded price
last_price = stock_quote['lastPrice']

print(f"Last traded price of {stock_symbol}: {last_price}")
