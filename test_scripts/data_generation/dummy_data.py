import numpy as np
import pandas as pd

def generate_dummy_stock_data(start_price=100, days=252, mu=0.0005, sigma=0.01):
    """
    Generates dummy stock price data using geometric Brownian motion.

    Parameters:
    - start_price (float): The starting price of the stock.
    - days (int): Number of days to simulate.
    - mu (float): Expected return.
    - sigma (float): Volatility of returns.

    Returns:
    - pd.Series: Simulated stock prices indexed by date.
    """
    dt = 1  # Time increment (daily)
    prices = [start_price]
    for _ in range(1, days):
        price = prices[-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.random.normal())
        prices.append(price)
    
    dates = pd.date_range(start='2020-01-01', periods=days)
    return pd.Series(prices, index=dates, name='Price')

def generate_dummy_signals(prices, short_window=20, long_window=50):
    """
    Generates buy and sell signals based on a moving average crossover strategy.

    Parameters:
    - prices (pd.Series): Stock price data.
    - short_window (int): Window for short-term moving average.
    - long_window (int): Window for long-term moving average.

    Returns:
    - pd.DataFrame: DataFrame containing the stock prices, moving averages, and signals.
    """
    signals = pd.DataFrame(index=prices.index)
    signals['Price'] = prices
    signals['Short_MA'] = prices.rolling(window=short_window, min_periods=1).mean()
    signals['Long_MA'] = prices.rolling(window=long_window, min_periods=1).mean()

    # Use .loc[] to avoid SettingWithCopyWarning
    signals['Signal'] = 0
    signals.loc[signals.index[short_window:], 'Signal'] = np.where(
        signals['Short_MA'][short_window:] > signals['Long_MA'][short_window:], 1, 0
    )
    signals['Positions'] = signals['Signal'].diff()
    
    return signals


def save_to_csv(data, filename):
    """
    Saves the given data to a CSV file.

    Parameters:
    - data (pd.DataFrame or pd.Series): The data to save.
    - filename (str): The name of the CSV file.
    """
    data.to_csv(filename)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    # Generate dummy stock price data
    stock_prices = generate_dummy_stock_data()

    # Generate dummy trading signals
    signals = generate_dummy_signals(stock_prices)

    # Save stock prices to CSV
    save_to_csv(stock_prices, "dummy_stock_prices.csv")

    # Save signals to CSV
    save_to_csv(signals, "dummy_signals.csv")
