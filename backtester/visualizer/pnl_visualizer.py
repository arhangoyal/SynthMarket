# visualizer/pnl_visualizer.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Optional
from datetime import datetime

class PnLVisualizer:
    def __init__(self, figsize=(15, 10)):
        self.figsize = figsize
        
    def calculate_pnl_metrics(self, trades: List[Dict], prices: List[float], timestamps: List[datetime]) -> pd.DataFrame:
        """
        Calculate realized and unrealized PnL over time
        """
        # Create DataFrame with time series
        df = pd.DataFrame({
            'timestamp': timestamps,
            'price': prices
        })
        
        # Ensure timestamp is datetime type and set as index
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        
        # Initialize PnL columns
        df['realized_pnl'] = 0.0
        df['unrealized_pnl'] = 0.0
        df['position'] = 0.0
        df['avg_entry_price'] = 0.0
        
        current_position = 0
        realized_pnl = 0
        position_cost = 0
        
        # Process trades
        for trade in trades:
            # Use the timestamp directly since it's already in datetime format
            trade_time = pd.to_datetime(trade['timestamp'])
            
            # Update position
            size = trade['size']
            side = trade['side']
            price = trade['price']
            
            trade_size = size if side == 'buy' else -size
            old_position = current_position
            current_position += trade_size
            
            # Calculate realized PnL for reducing trades
            if (old_position > 0 and trade_size < 0) or (old_position < 0 and trade_size > 0):
                reducing_size = min(abs(old_position), abs(trade_size))
                realized_pnl += reducing_size * (price - position_cost/old_position) * (-1 if old_position > 0 else 1)
            
            # Update position cost
            if current_position != 0:
                position_cost = (position_cost + trade_size * price)
            
            # Find the closest timestamp in our index
            idx = df.index.get_indexer([trade_time], method='nearest')[0]
            trade_time = df.index[idx]
            
            # Update DataFrame at and after this timestamp
            df.loc[trade_time:, 'position'] = current_position
            df.loc[trade_time:, 'realized_pnl'] = realized_pnl
            if current_position != 0:
                df.loc[trade_time:, 'avg_entry_price'] = position_cost / current_position
            
        # Calculate unrealized PnL
        df['unrealized_pnl'] = df['position'] * (df['price'] - df['avg_entry_price'])
        
        df['total_pnl'] = df['realized_pnl'] + df['unrealized_pnl']
        if len(df) > 1:
            df['total_pnl'][0] = df['realized_pnl'][1] + df['unrealized_pnl'][0]
        
        return df
        
    def plot_pnl(self, df: pd.DataFrame, strategy_name: str = '', save_path: Optional[str] = None):
        """
        Plot PnL metrics
        """
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=self.figsize)
        
        # Plot prices and position
        ax1.plot(df.index, df['price'], label='Price', color='black', alpha=0.5)
        ax1t = ax1.twinx()
        ax1t.fill_between(df.index, df['position'], 0, alpha=0.3, label='Position')
        ax1.set_title(f'{strategy_name} - Price and Position')
        ax1.legend(loc='upper left')
        ax1t.legend(loc='upper right')
        
        # Plot PnL components
        ax2.plot(df.index, df['unrealized_pnl'], label='Unrealized PnL', color='blue', alpha=0.5)
        ax2.set_title('PnL Components')
        ax2.legend()
        ax2.grid(True)
        
        # Plot total PnL
        ax3.plot(df.index, df['total_pnl'], label='Total PnL', color='red')
        ax3.set_title('Total PnL')
        ax3.legend()
        ax3.grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
        plt.show()