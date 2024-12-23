from typing import Optional
from datetime import datetime
import numpy as np
from ..base.participant import Participant
from ..configs.participant_configs import StatArbConfig

class StatisticalArbitrageTrader(Participant):
    def __init__(self, config: StatArbConfig):
        super().__init__(
            initial_capital=config.initial_capital,
            max_position_size=config.max_position_size,
            risk_limit=config.risk_limit
        )
        self.config = config
        self.price_history = []
        self.mean = None
        self.std = None
        
    def calculate_zscore(self, price: float) -> Optional[float]:
        """Calculate z-score of current price."""
        if len(self.price_history) < self.config.lookback_period:
            return None
            
        # Calculate rolling statistics
        self.mean = np.mean(self.price_history[-self.config.lookback_period:])
        self.std = np.std(self.price_history[-self.config.lookback_period:])
        
        if self.std == 0:
            return None
            
        return (price - self.mean) / self.std
        
    def should_enter_long(self, zscore: float) -> bool:
        """Determine if we should enter a long position."""
        return (zscore < -self.config.entry_threshold and 
                self.position.quantity <= 0)
                
    def should_enter_short(self, zscore: float) -> bool:
        """Determine if we should enter a short position."""
        return (zscore > self.config.entry_threshold and 
                self.position.quantity >= 0)
                
    def should_exit(self, zscore: float) -> bool:
        """Determine if we should exit current position."""
        if self.position.quantity > 0:
            return zscore >= -self.config.exit_threshold
        elif self.position.quantity < 0:
            return zscore <= self.config.exit_threshold
        return False
        
    def on_market_update(self, price: float, volume: float, timestamp: datetime):
        """Handle market updates and make trading decisions."""
        # Update position metrics
        self.update_position(price)
        
        # Update price history
        self.price_history.append(price)
        if len(self.price_history) > self.config.lookback_period * 2:
            self.price_history.pop(0)
            
        # Calculate z-score
        zscore = self.calculate_zscore(price)
        if zscore is None:
            return
            
        # Check for exit conditions first
        if self.position.quantity != 0 and self.should_exit(zscore):
            # Exit position
            exit_size = -self.position.quantity
            self.execute_trade(price, exit_size, timestamp)
            return
            
        # Check entry conditions
        if self.should_enter_long(zscore):
            # Enter long position
            self.execute_trade(price, self.config.position_size, timestamp)
            
        elif self.should_enter_short(zscore):
            # Enter short position
            self.execute_trade(price, -self.config.position_size, timestamp)
            
    def calculate_signals(self):
        """Calculate additional trading signals and indicators."""
        if len(self.price_history) < self.config.lookback_period:
            return None
            
        # Calculate rolling volatility
        volatility = np.std(self.price_history[-20:])
        
        # Calculate momentum
        returns = np.diff(self.price_history[-20:])
        momentum = np.sum(returns)
        
        return {
            'volatility': volatility,
            'momentum': momentum,
            'mean': self.mean,
            'std': self.std
        }