from alpha_vantage.timeseries import TimeSeries

# Replace 'YOUR_API_KEY' with your Alpha Vantage API key
API_KEY = 'RR79VSLOZJIX0KHG'

# Initialize Alpha Vantage API
ts = TimeSeries(key=API_KEY, output_format='pandas')

# Replace 'AAPL' with the actual stock symbol you want to fetch
stock_symbol = 'TCS'

# Fetch real-time stock data
data, meta_data = ts.get_quote_endpoint(symbol=stock_symbol)

# Extract the current price
current_price = data['05. price'][0]
print(current_price)
print(f"Current price of {stock_symbol}: {current_price}")
