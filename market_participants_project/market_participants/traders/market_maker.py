from typing import Tuple, Optional
from datetime import datetime
import numpy as np
from ..base.participant import Participant
from ..configs.participant_configs import MarketMakerConfig

class MarketMaker(Participant):
    def __init__(self, config: MarketMakerConfig):
        super().__init__(
            initial_capital=config.initial_capital,
            max_position_size=config.max_position_size,
            risk_limit=config.risk_limit
        )
        self.config = config
        self.last_price = None
        self.recent_prices = []
        self.recent_volumes = []
        
    def calculate_quotes(self, mid_price: float) -> Tuple[float, float]:
        """Calculate bid and ask prices based on spread and inventory."""
        # Base spread calculation
        half_spread = mid_price * (self.config.spread_width / 2)
        
        # Simple quote calculation
        bid = mid_price - half_spread
        ask = mid_price + half_spread
        
        return bid, ask
        
    def should_trade(self, price: float, volume: float) -> bool:
        """Determine if market conditions are suitable for trading."""
        # Always allow trading unless position limits are hit
        if abs(self.position.quantity) >= self.config.max_inventory:
            return False
        return True
        
    def on_market_update(self, price: float, volume: float, timestamp: datetime):
        """Handle market updates and make trading decisions."""
        self.recent_prices.append(price)
        if len(self.recent_prices) > 100:
            self.recent_prices.pop(0)
            
        # Update position metrics
        self.update_position(price)
        
        # Calculate quotes
        bid, ask = self.calculate_quotes(price)
        
        # Fixed trade size for simplicity
        trade_size = self.config.min_trade_size
        
        if self.last_price is not None and self.should_trade(price, volume):
            # Price moved above our last ask - sell
            if price > self.last_price + (self.config.spread_width * price):
                if self.position.quantity > -self.config.max_inventory:
                    self.execute_trade(price, -trade_size, timestamp)
                    
            # Price moved below our last bid - buy
            elif price < self.last_price - (self.config.spread_width * price):
                if self.position.quantity < self.config.max_inventory:
                    self.execute_trade(price, trade_size, timestamp)
                    
        self.last_price = price
        
        # Manage inventory if position is too large
        self.manage_inventory(price, timestamp)
        
    def manage_inventory(self, current_price: float, timestamp: datetime):
        """Actively manage inventory to maintain target position."""
        if abs(self.position.quantity) > self.config.max_inventory * 0.8:  # 80% of max
            # Calculate reduction needed
            reduction = -np.sign(self.position.quantity) * self.config.min_trade_size
            self.execute_trade(current_price, reduction, timestamp)