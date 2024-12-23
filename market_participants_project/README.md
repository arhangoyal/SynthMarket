# Market Participants Simulation Project

## Overview
This project simulates different types of market participants (traders) interacting in a financial market. It includes implementations of various trading strategies and provides a framework for testing and analyzing their performance.

## Project Structure
```
market_participants_project/
├── market_participants/
│   ├── __init__.py
│   ├── base/
│   │   ├── __init__.py
│   │   └── participant.py         # Base class for all trading participants
│   ├── configs/
│   │   ├── __init__.py
│   │   └── participant_configs.py # Configuration classes for each trader type
│   ├── traders/
│   │   ├── __init__.py
│   │   ├── market_maker.py       # Market making strategy implementation
│   │   └── position_taker.py     # Position taking strategy implementation
│   └── utils/
│       ├── __init__.py
│       └── metrics.py            # Trading metrics calculations
├── tests/
│   ├── __init__.py
│   └── test_traders.py          # Main testing script
├── data/
│   └── heston_tick_supported_30s_data.csv  # Sample market data
├── setup.py                     # Project installation configuration
└── requirements.txt            # Project dependencies
```

## Trading Strategies

### 1. Market Maker
- Provides liquidity by maintaining bid/ask quotes
- Aims to profit from the spread while managing inventory
- Key parameters:
  - spread_width: Width of bid-ask spread (e.g., 0.0005 = 0.05%)
  - max_inventory: Maximum position size allowed
  - min_trade_size/max_trade_size: Trade size limits

### 2. Position Taker
- Takes directional positions based on momentum signals
- Uses stop-loss and take-profit levels
- Key parameters:
  - momentum_period: Lookback period for momentum calculation
  - entry_threshold: Required momentum for position entry
  - stop_loss/take_profit: Risk management levels

## Installation and Setup

1. Create a virtual environment:
```bash
python -m venv project_env
source project_env/bin/activate  # On Unix/MacOS
# or
.\project_env\Scripts\activate   # On Windows
```

2. Install the package in development mode:
```bash
pip install -e .
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Tests

Run the main test script:
```bash
python tests/test_traders.py
```

## Understanding the Output

The test output shows performance metrics for each trading strategy:

### Market Maker Metrics
```
Market Maker Final Results:
- Total Trades: Number of trades executed
- Final Position: End-of-period position
- Total PnL: Total profit/loss
- Avg PnL per Trade: Average profit per trade
- Sharpe Ratio: Risk-adjusted return metric
- Max Position Held: Largest absolute position
```

### Position Taker Metrics
```
Position Taker Results:
- Total Trades: Number of trades executed
- Final Position: End-of-period position
- Total PnL: Total profit/loss
- Sharpe Ratio: Risk-adjusted return metric
```

## Key Performance Indicators (KPIs)

1. Trading Activity
   - Total number of trades
   - Average trade size
   - Position turnover

2. Risk Metrics
   - Maximum position held
   - Position duration
   - Maximum drawdown

3. Profitability
   - Total PnL
   - Average PnL per trade
   - Sharpe ratio

## Strategy Performance Analysis

The project implements and tests four different trading strategies on simulated market data. Here's how they performed:

### Strategy Results

1. **Market Maker**
- Most active with 2,572 trades
- Consistent but breakeven performance (PnL: $0.10)
- Good risk control with max position ±8.00 units
- Best suited for providing continuous liquidity

2. **Statistical Arbitrage**
- Selective trading with 97 trades
- Conservative position management (max ±5.00 units)
- Slight loss (PnL: -$0.75)
- Good for mean-reversion opportunities

3. **TWAP (Time-Weighted Average Price)**
- Limited trades (19) but large positions
- Significant losses (PnL: -$672.40)
- Needs parameter optimization
- Suitable for time-sensitive executions

4. **VWAP (Volume-Weighted Average Price)**
- Moderate activity with 747 trades
- Best performer (PnL: $49.14)
- Largest positions (up to 74.75 units)
- Best for volume-sensitive executions

### Key Insights
- VWAP showed best overall performance
- Market Making provided most stable execution
- Position sizing crucial for strategy success
- Market impact significantly affects large orders
- Risk management parameters need careful tuning

## Common Issues and Solutions

1. No Trading Activity
   - Check spread_width parameter
   - Verify price movements exceed spread
   - Ensure position limits aren't too restrictive

2. Poor Performance
   - Adjust entry/exit thresholds
   - Review risk management parameters
   - Consider market conditions

3. High Risk Exposure
   - Reduce max_inventory
   - Tighten stop-loss levels
   - Implement more aggressive inventory management

## Future Improvements

1. Enhanced Risk Management
   - Dynamic position limits
   - Volatility-based sizing
   - Correlation analysis

2. Performance Optimization
   - Event-driven architecture
   - Real-time analysis
   - Portfolio management