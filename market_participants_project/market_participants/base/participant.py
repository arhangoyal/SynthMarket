from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np
from datetime import datetime

@dataclass
class Position:
    quantity: float = 0.0
    avg_entry_price: float = 0.0
    realized_pnl: float = 0.0
    unrealized_pnl: float = 0.0
    last_update_price: float = 0.0
    
    def update_unrealized_pnl(self, current_price: float):
        if self.quantity != 0:
            self.unrealized_pnl = (current_price - self.avg_entry_price) * self.quantity
        self.last_update_price = current_price

class Participant(ABC):
    def __init__(self, 
                 initial_capital: float = 1000000.0,
                 max_position_size: float = 1000.0,
                 risk_limit: float = 100000.0):
        self.capital = initial_capital
        self.max_position_size = max_position_size
        self.risk_limit = risk_limit
        self.position = Position()
        
        # Trading metrics
        self.trades: List[Dict] = []
        self.trade_history: List[Dict] = []
        self.metrics = {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'max_drawdown': 0.0,
            'sharpe_ratio': 0.0,
            'returns': []
        }
        
    def execute_trade(self, price: float, quantity: float, timestamp: Optional[datetime] = None) -> bool:
        """
        Execute a trade and update position
        
        Args:
            price: Execution price
            quantity: Quantity to trade (positive for buy, negative for sell)
            timestamp: Optional timestamp for the trade
        
        Returns:
            bool: Whether trade was successful
        """
        # Check position limits
        if abs(self.position.quantity + quantity) > self.max_position_size:
            return False
            
        # Check risk limits
        potential_exposure = abs((self.position.quantity + quantity) * price)
        if potential_exposure > self.risk_limit:
            return False
            
        # Update position
        if self.position.quantity == 0:
            self.position.avg_entry_price = price
            self.position.quantity = quantity
        else:
            # Calculate new average entry price
            total_cost = (self.position.quantity * self.position.avg_entry_price) + (quantity * price)
            new_position = self.position.quantity + quantity
            if new_position != 0:
                self.position.avg_entry_price = total_cost / new_position
            self.position.quantity = new_position
            
        # Record trade
        trade_record = {
            'timestamp': timestamp or datetime.now(),
            'price': price,
            'quantity': quantity,
            'position': self.position.quantity,
            'avg_entry': self.position.avg_entry_price
        }
        self.trades.append(trade_record)
        self.metrics['total_trades'] += 1
        
        return True
        
    def update_position(self, current_price: float):
        """Update position metrics with current market price"""
        self.position.update_unrealized_pnl(current_price)
        
    def get_total_pnl(self) -> float:
        """Get total PnL (realized + unrealized)"""
        return self.position.realized_pnl + self.position.unrealized_pnl
        
    def calculate_metrics(self):
        """Calculate trading metrics"""
        if not self.trades:
            return
            
        # Calculate returns
        prices = [trade['price'] for trade in self.trades]
        returns = np.diff(np.log(prices))
        self.metrics['returns'] = returns.tolist()
        
        # Sharpe ratio (assuming daily)
        if len(returns) > 1:
            self.metrics['sharpe_ratio'] = np.sqrt(252) * (np.mean(returns) / np.std(returns))
            
        # Max drawdown
        cumulative_returns = np.cumsum(returns)
        rolling_max = np.maximum.accumulate(cumulative_returns)
        drawdowns = rolling_max - cumulative_returns
        self.metrics['max_drawdown'] = np.max(drawdowns)
        
    @abstractmethod
    def on_market_update(self, price: float, volume: float, timestamp: datetime):
        """
        Handle market updates - must be implemented by specific strategies
        
        Args:
            price: Current market price
            volume: Current market volume
            timestamp: Update timestamp
        """
        pass