# run_backtest.py
import pandas as pd
import os
from pathlib import Path
from strategies.l2_orderbook_strategy import L2OrderbookStrategy
from backtesters.l2_backtester import L2Backtester
from visualizer.pnl_visualizer import PnLVisualizer

def main():
    # Load L2 data
    current_file_path = os.path.abspath(__file__)
    parent_dir = os.path.dirname(os.path.dirname(current_file_path))
    data_path = os.path.join(parent_dir, 'simulation_output', 'process_simulation_output_heston.csv')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"L2 data file not found: {data_path}")
        
    data = pd.read_csv(data_path)
    # Convert datetime strings to pandas datetime objects
    data['Datetime'] = pd.to_datetime(data['Datetime'])
    print(f"Loaded L2 data: {len(data)} rows")
    
    # Strategy parameters
    parameters = {
        'position_limit': 100,
        'imbalance_threshold': 0.3,
        'trade_size': 2.0
    }
    
    # Initialize strategy and backtester
    strategy = L2OrderbookStrategy(parameters)
    backtester = L2Backtester(data, strategy)
    
    # Run backtest
    print("\nRunning backtest...")
    results = backtester.run()
    
    # Print results
    print("\nBacktest Results:")
    for metric, value in results.items():
        print(f"{metric}: {value}")

    # Initialize visualizer
    visualizer = PnLVisualizer(figsize=(15, 10))
    
    # Use actual timestamps from the data
    timestamps = data['Datetime'].tolist()
    
    # Create output directory if it doesn't exist
    output_dir = Path('data/output')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Calculate and plot PnL metrics
    try:
        pnl_df = visualizer.calculate_pnl_metrics(
            trades=backtester.fills,
            prices=data['Price'].tolist(),
            timestamps=timestamps
        )
        
        visualizer.plot_pnl(
            df=pnl_df,
            strategy_name='L2 Orderbook Strategy',
            save_path=output_dir / 'l2_strategy_pnl.png'
        )
        
        print("\nVisualization has been saved to data/output/l2_strategy_pnl.png")
        
    except Exception as e:
        print(f"\nError generating visualization: {str(e)}")
        raise

if __name__ == "__main__":
    main()