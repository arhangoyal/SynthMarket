# backtesters/l2_backtester.py
from typing import Dict
import pandas as pd
from utils.orderbook import OrderBook

class L2Backtester:
    def __init__(self, data: pd.DataFrame, strategy):
        """
        Initialize L2 backtester
        
        Args:
            data: DataFrame with L2 orderbook data
            strategy: Trading strategy instance
        """
        self.data = data
        self.strategy = strategy
        self.orderbook = OrderBook()
        self.fills = []
        
    def update_orderbook(self, market_depth: pd.Series):
        """Update internal orderbook state"""
        self.orderbook = OrderBook()  # Reset orderbook
        
        # Add bid levels
        for i in range(1, 6):
            price = market_depth[f'BidPrice_{i}']
            size = market_depth[f'BidSize_{i}']
            self.orderbook.add_bid(price, size)
            
        # Add ask levels
        for i in range(1, 6):
            price = market_depth[f'AskPrice_{i}']
            size = market_depth[f'AskSize_{i}']
            self.orderbook.add_ask(price, size)
            
    def execute_order(self, size: float, side: str, market_depth: pd.Series) -> Dict:
        """
        Execute order with market impact simulation
        
        Returns:
            Dict containing fill details
        """
        # Use best bid/ask for execution
        if side == 'buy':
            price, available_volume = self.orderbook.get_best_ask()
        else:
            price, available_volume = self.orderbook.get_best_bid()
            
        # Simulate market impact
        filled_size = min(size, available_volume)
        
        if filled_size > 0:
            return {
                'timestamp': market_depth['Datetime'],  # Changed from 'Time' to 'Datetime'
                'side': side,
                'price': price,
                'size': filled_size
            }
        return None
        
    def run(self) -> Dict:
        """
        Run backtest
        
        Returns:
            Dict containing backtest results
        """
        for idx, row in self.data.iterrows():
            # Update orderbook state
            self.update_orderbook(row)
            
            # Get strategy signal
            should_trade, side, size = self.strategy.generate_signal(row)
            
            if should_trade:
                # Execute order
                fill = self.execute_order(size, side, row)
                if fill:
                    self.strategy.update_position(fill['size'], fill['side'])
                    self.fills.append(fill)
                    
        return self.calculate_results()
        
    def calculate_results(self) -> Dict:
        """Calculate backtest results"""
        if not self.fills:
            return {}
            
        fills_df = pd.DataFrame(self.fills)
        
        # Calculate basic metrics
        results = {
            'total_trades': len(self.fills),
            'final_position': self.strategy.position,
            'avg_trade_size': fills_df['size'].mean()
        }
        
        # Add PnL calculations if needed
        if 'price' in fills_df.columns:
            results['avg_price'] = fills_df['price'].mean()
            
        return results