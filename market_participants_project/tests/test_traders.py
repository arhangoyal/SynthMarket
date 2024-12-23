# tests/test_traders.py
import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from market_participants.traders import (
    MarketMaker, 
    StatisticalArbitrageTrader, 
    PositionTaker,
    TWAPTrader,
    VWAPTrader
)
from market_participants.configs.participant_configs import (
    MarketMakerConfig,
    StatArbConfig,
    PositionTakerConfig,
    TWAPConfig,
    VWAPConfig
)

def load_and_prepare_data(file_path: str) -> pd.DataFrame:
    """Load and prepare the data for testing."""
    data_path = os.path.join(project_root, 'data', file_path)
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at: {data_path}")
        
    df = pd.read_csv(data_path)
    df['datetime'] = pd.to_datetime('2024-01-01') + pd.to_timedelta(df['Time'], unit='D')
    return df

def test_market_maker(data: pd.DataFrame):
    """Test MarketMaker strategy"""
    print("\nTesting Market Maker Strategy...")
    
    config = MarketMakerConfig(
        spread_width=0.0005,          # 0.05% spread
        inventory_target=0.0,
        max_inventory=10.0,
        min_trade_size=0.5,
        max_trade_size=1.0,
        initial_capital=1000000.0,
        risk_limit=100000.0
    )
    
    market_maker = MarketMaker(config)
    positions = []
    pnls = []
    
    # Process market updates
    for idx, row in data.iterrows():
        market_maker.on_market_update(
            price=row['Price'],
            volume=1.0,
            timestamp=row['datetime']
        )
        
        positions.append(market_maker.position.quantity)
        pnls.append(market_maker.get_total_pnl())
        
        if idx % 100 == 0:
            print(f"\nUpdate {idx}:")
            print(f"Price: {row['Price']:.2f}")
            print(f"Position: {market_maker.position.quantity:.2f}")
            print(f"Total Trades: {market_maker.metrics['total_trades']}")
            print(f"Total PnL: {market_maker.get_total_pnl():.2f}")
    
    return positions, pnls

def test_stat_arb(data: pd.DataFrame):
    """Test Statistical Arbitrage strategy"""
    print("\nTesting Statistical Arbitrage Strategy...")
    
    config = StatArbConfig(
        lookback_period=50,
        entry_threshold=2.0,
        exit_threshold=0.0,
        position_size=5.0,
        initial_capital=1000000.0,
        max_position_size=20.0,
        risk_limit=100000.0
    )
    
    stat_arb = StatisticalArbitrageTrader(config)
    positions = []
    pnls = []
    
    for idx, row in data.iterrows():
        stat_arb.on_market_update(
            price=row['Price'],
            volume=1.0,
            timestamp=row['datetime']
        )
        
        positions.append(stat_arb.position.quantity)
        pnls.append(stat_arb.get_total_pnl())
        
        if idx % 100 == 0:
            print(f"\nUpdate {idx}:")
            print(f"Price: {row['Price']:.2f}")
            print(f"Position: {stat_arb.position.quantity:.2f}")
            print(f"Total Trades: {stat_arb.metrics['total_trades']}")
            print(f"Total PnL: {stat_arb.get_total_pnl():.2f}")
    
    return positions, pnls

def test_twap(data: pd.DataFrame):
    """Test TWAP strategy"""
    print("\nTesting TWAP Strategy...")
    
    config = TWAPConfig(
        target_position=100.0,
        start_time="09:30:00",
        end_time="16:00:00",
        num_slices=20,
        deviation_threshold=0.02,
        initial_capital=1000000.0,
        max_position_size=100.0,
        risk_limit=100000.0
    )
    
    twap = TWAPTrader(config)
    positions = []
    pnls = []
    
    for idx, row in data.iterrows():
        twap.on_market_update(
            price=row['Price'],
            volume=1.0,
            timestamp=row['datetime']
        )
        
        positions.append(twap.position.quantity)
        pnls.append(twap.get_total_pnl())
        
        if idx % 100 == 0:
            print(f"\nUpdate {idx}:")
            print(f"Price: {row['Price']:.2f}")
            print(f"Position: {twap.position.quantity:.2f}")
            print(f"Total Trades: {twap.metrics['total_trades']}")
            print(f"Total PnL: {twap.get_total_pnl():.2f}")
    
    return positions, pnls

def test_vwap(data: pd.DataFrame):
    """Test VWAP strategy"""
    print("\nTesting VWAP Strategy...")
    
    config = VWAPConfig(
        target_position=100.0,
        start_time="09:30:00",
        end_time="16:00:00",
        participation_rate=0.1,
        max_participation_rate=0.3,
        initial_capital=1000000.0,
        max_position_size=100.0,
        risk_limit=100000.0
    )
    
    vwap = VWAPTrader(config)
    positions = []
    pnls = []
    
    for idx, row in data.iterrows():
        vwap.on_market_update(
            price=row['Price'],
            volume=1.0,
            timestamp=row['datetime']
        )
        
        positions.append(vwap.position.quantity)
        pnls.append(vwap.get_total_pnl())
        
        if idx % 100 == 0:
            print(f"\nUpdate {idx}:")
            print(f"Price: {row['Price']:.2f}")
            print(f"Position: {vwap.position.quantity:.2f}")
            print(f"Total Trades: {vwap.metrics['total_trades']}")
            print(f"Total PnL: {vwap.get_total_pnl():.2f}")
    
    return positions, pnls

def plot_strategy_comparison(data, results_dict):
    """Plot comparison of all strategies"""
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12))
    
    # Plot price
    ax1.plot(data['Price'], label='Price', color='black', alpha=0.5)
    ax1.set_title('Price Movement')
    ax1.legend()
    ax1.grid(True)
    
    # Plot positions
    for name, (positions, _) in results_dict.items():
        ax2.plot(positions, label=f'{name} Position')
    ax2.set_title('Position Comparison')
    ax2.legend()
    ax2.grid(True)
    
    # Plot PnLs
    for name, (_, pnls) in results_dict.items():
        ax3.plot(pnls, label=f'{name} PnL')
    ax3.set_title('PnL Comparison')
    ax3.legend()
    ax3.grid(True)
    
    plt.tight_layout()
    
    # Save plot
    plot_path = os.path.join(project_root, 'output', 'strategy_comparison.png')
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    plt.savefig(plot_path)
    plt.close()

def print_strategy_summary(results_dict):
    """Print summary statistics for all strategies"""
    print("\n=== Strategy Comparison Summary ===")
    
    for name, (positions, pnls) in results_dict.items():
        print(f"\n{name} Strategy:")
        print(f"Max Position: {max(abs(np.array(positions))):.2f}")
        print(f"Final PnL: {pnls[-1]:.2f}")
        print(f"Max Drawdown: {min(pnls):.2f}")
        print(f"Best PnL: {max(pnls):.2f}")
        
        # Calculate Sharpe ratio
        pnl_returns = np.diff(pnls)
        if len(pnl_returns) > 0 and np.std(pnl_returns) > 0:
            sharpe = np.mean(pnl_returns) / np.std(pnl_returns) * np.sqrt(252)
            print(f"Sharpe Ratio: {sharpe:.2f}")

def main():
    try:
        # Load and prepare data
        data = load_and_prepare_data('heston_tick_supported_30s_data.csv')
        print("Data loaded successfully")
        print(f"Data shape: {data.shape}")
        print("\nFirst few rows:")
        print(data.head())
        
        # Run all strategy tests
        results = {}
        
        results['Market Maker'] = test_market_maker(data)
        results['Stat Arb'] = test_stat_arb(data)
        results['TWAP'] = test_twap(data)
        results['VWAP'] = test_vwap(data)
        
        # Generate comparison plots
        plot_strategy_comparison(data, results)
        
        # Print summary statistics
        print_strategy_summary(results)
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        raise

if __name__ == "__main__":
    main()