# Dummy Data Generation for Trading Strategies

This README provides an overview of the dummy data generation for testing trading strategies. The generated data includes daily stock prices and trading signals based on a Moving Average Crossover strategy.

## Generated CSV Files

### 1. `dummy_stock_prices.csv`
- **Content**: Daily stock prices generated using a geometric Brownian motion model.
- **Columns**:
  - `Date`: Trading day date.
  - `Price`: Closing stock price.
- **Usage**: Provides historical price information for backtesting trading strategies.

### 2. `dummy_signals.csv`
- **Content**: Trading signals based on a Moving Average Crossover strategy.
- **Columns**:
  - `Date`: Trading day date.
  - `Price`: Closing stock price.
  - `Short_MA`: Short-term moving average.
  - `Long_MA`: Long-term moving average.
  - `Signal`: Buy (1) or hold (0) signal.
  - `Positions`: Changes in position (1: open, -1: close, NaN: no change).
- **Usage**: Evaluates strategy effectiveness by indicating when to enter or exit positions.

## How to Use the Data
- **Backtesting**: Use `dummy_stock_prices.csv` for historical price analysis and `dummy_signals.csv` for simulating trading decisions.
- **Technical Analysis**: Visualize moving averages and signals to assess crossover strategy effectiveness.

---
