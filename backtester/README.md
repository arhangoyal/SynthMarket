# L2 Orderbook Backtester

A Python-based backtesting framework for developing and testing trading strategies using Level 2 (L2) orderbook data. This backtester simulates realistic market conditions by incorporating orderbook depth, market impact, and execution logic.

## Directory Structure
```
backtester/
├── data/
│   └── l2_data/          # Store your L2 orderbook data here
├── strategies/           # Trading strategy implementations
├── backtesters/         # Backtesting engine components
├── utils/               # Utility functions and classes
└── run_backtest.py     # Main execution script
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd backtester
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your L2 orderbook data in CSV format in the `data/l2_data/` directory.

2. Configure strategy parameters in `run_backtest.py`:
```python
parameters = {
    'position_limit': 100,
    'imbalance_threshold': 0.3,
    'trade_size': 1.0
}
```

3. Run the backtest:
```bash
python run_backtest.py
```

## Data Format

The backtester expects L2 data in CSV format with the following columns:
- Time: Timestamp
- Price: Mid price
- BidPrice_1..5: Bid prices for levels 1-5
- BidSize_1..5: Bid sizes for levels 1-5
- AskPrice_1..5: Ask prices for levels 1-5
- AskSize_1..5: Ask sizes for levels 1-5
- BidAskSpread: Spread between best bid and ask

## Creating New Strategies

1. Create a new strategy class in the `strategies` directory:
```python
from backtester.backtesters.l2_backtester import StrategyBase

class MyStrategy(StrategyBase):
    def __init__(self, parameters=None):
        super().__init__()
        self.parameters = parameters or {}
        
    def on_market_depth(self, market_depth):
        # Implement your strategy logic here
        pass
```

2. Update `run_backtest.py` to use your strategy:
```python
from strategies.my_strategy import MyStrategy
strategy = MyStrategy(parameters)
```

## Features

- Full L2 orderbook simulation
- Realistic order execution with market impact
- Position tracking and risk management
- Performance analytics
- Extensible strategy framework

## Results Interpretation

The backtester provides several key metrics to evaluate strategy performance:

- total_trades: Number of executed trades during the simulation period
- final_position: Net position at the end of the backtest (positive = long, negative = short)
- avg_trade_size: Average size of executed trades
- avg_price: Average execution price across all trades

Example output:
```
Backtest Results:
total_trades: 34
final_position: -6.0
avg_trade_size: 1.0
avg_price: 118.81
```

This indicates the strategy executed 34 trades with consistent trade sizing (1.0), ending with a net short position of 6 units at an average execution price of 118.81.