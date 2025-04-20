import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Fetch BTC/USD price data from CoinGecko API
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
params = {
    'vs_currency': 'usd',
    'days': '365',
    'interval': 'daily'
}

try:
    response = requests.get(url, params=params)
    data = response.json()
    
    # Extract prices and dates
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    x = df.set_index('date')['price']
    
    # Calculate daily returns (percentage change)
    returns = x.pct_change().dropna()
    
    # Calculate risk metrics (annualized)
    risk = np.std(returns) * np.sqrt(252)  # Annualized volatility
    sharpe = (np.mean(returns) / np.std(returns)) * np.sqrt(252)
    
    print(f"Annualized Volatility: {risk:.4f}")
    print(f"Sharpe Ratio: {sharpe:.4f}")
    
    # Plot the price data
    plt.figure(figsize=(12, 6))
    plt.plot(x.index, x, label='BTC/USD Price')
    plt.title('BTC/USD Price (1 Year)')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.legend()
    plt.savefig('btc_price.png')
    plt.close()
    
except Exception as e:
    print(f"Error: {e}")
    print("Possible issues:")
    print("- No internet connection")
    print("- CoinGecko API rate limit reached (wait a minute)")
