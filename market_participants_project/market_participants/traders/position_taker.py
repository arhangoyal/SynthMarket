from datetime import datetime
import numpy as np
from ..base.participant import Participant
from ..configs.participant_configs import PositionTakerConfig

class PositionTaker(Participant):
    def __init__(self, config: PositionTakerConfig):
        super().__init__(
            initial_capital=config.initial_capital,
            max_position_size=config.max_position_size,
            risk_limit=config.risk_limit
        )
        self.config = config
        self.price_history = []
        self.entry_price = None
        
    def calculate_signals(self) -> dict:
        """Calculate trading signals based on price history."""
        if len(self.price_history) < self.config.momentum_period:
            return {'momentum': 0, 'volatility': 0}
            
        prices = np.array(self.price_history[-self.config.momentum_period:])
        returns = np.diff(np.log(prices))  # Use log returns for better statistical properties
        
        momentum = np.mean(returns) * np.sqrt(252)  # Annualized momentum
        volatility = np.std(returns) * np.sqrt(252)  # Annualized volatility
        
        return {
            'momentum': momentum,
            'volatility': volatility
        }
        
    def calculate_position_size(self, signals: dict) -> float:
        """Calculate position size based on volatility and momentum."""
        if signals['volatility'] == 0:
            return 0
            
        # Scale position size inversely with volatility
        volatility_scalar = min(1.0, 0.2 / signals['volatility'])
        
        # Scale with momentum strength
        momentum_scalar = min(1.0, abs(signals['momentum']) / self.config.entry_threshold)
        
        # Calculate base position size
        base_size = self.config.max_position_size * 0.2  # Start with 20% of max
        
        # Scale position size
        position_size = base_size * volatility_scalar * momentum_scalar
        
        return position_size
        
    def check_stop_loss(self, current_price: float) -> bool:
        """Check if stop loss has been hit."""
        if self.entry_price is None or self.position.quantity == 0:
            return False
            
        if self.position.quantity > 0:
            return current_price <= self.entry_price * (1 - self.config.stop_loss)
        else:
            return current_price >= self.entry_price * (1 + self.config.stop_loss)
            
    def check_take_profit(self, current_price: float) -> bool:
        """Check if take profit has been hit."""
        if self.entry_price is None or self.position.quantity == 0:
            return False
            
        if self.position.quantity > 0:
            return current_price >= self.entry_price * (1 + self.config.take_profit)
        else:
            return current_price <= self.entry_price * (1 - self.config.take_profit)
            
    def on_market_update(self, price: float, volume: float, timestamp: datetime):
        """Handle market updates and make trading decisions."""
        self.update_position(price)
        self.price_history.append(price)
        
        # Keep price history at manageable size
        if len(self.price_history) > max(self.config.momentum_period, self.config.volatility_period) * 2:
            self.price_history.pop(0)
            
        # Check exit conditions if in position
        if self.position.quantity != 0:
            if self.check_stop_loss(price) or self.check_take_profit(price):
                self.execute_trade(price, -self.position.quantity, timestamp)
                self.entry_price = None
                return
                
        # Calculate signals
        signals = self.calculate_signals()
        if not signals['momentum']:  # Not enough data
            return
            
        # Entry logic
        if self.position.quantity == 0:  # Not in position
            if abs(signals['momentum']) > self.config.entry_threshold:
                # Calculate position size
                position_size = self.calculate_position_size(signals)
                
                # Enter position in direction of momentum
                trade_size = position_size * np.sign(signals['momentum'])
                
                if abs(trade_size) >= 1.0:  # Only trade if size is meaningful
                    if self.execute_trade(price, trade_size, timestamp):
                        self.entry_price = price