# market_participants/traders/vwap.py

from datetime import datetime, time
import numpy as np
from collections import deque
from ..base.participant import Participant
from ..configs.participant_configs import VWAPConfig

class VWAPTrader(Participant):
    def __init__(self, config: VWAPConfig):
        super().__init__(
            initial_capital=config.initial_capital,
            max_position_size=config.max_position_size,
            risk_limit=config.risk_limit
        )
        self.config = config
        self.volume_history = deque(maxlen=100)  # Rolling volume history
        self.price_volume_history = deque(maxlen=100)  # Price-volume history
        
        # Parse trading window times
        self.start_time = datetime.strptime(config.start_time, "%H:%M:%S").time()
        self.end_time = datetime.strptime(config.end_time, "%H:%M:%S").time()
        
        # Trading state
        self.total_volume = 0
        self.participation_volume = 0
        
    def calculate_vwap(self) -> float:
        """Calculate VWAP based on historical data."""
        if not self.price_volume_history:
            return None
            
        total_pv = sum(p * v for p, v in self.price_volume_history)
        total_v = sum(v for _, v in self.price_volume_history)
        
        return total_pv / total_v if total_v > 0 else None
        
    def calculate_target_trade_size(self, current_volume: float) -> float:
        """Calculate target trade size based on participation rate."""
        # Calculate current participation rate
        current_rate = (self.participation_volume / self.total_volume 
                       if self.total_volume > 0 else 0)
        
        # Adjust participation rate if we're behind/ahead of target
        participation_rate = self.config.participation_rate
        if current_rate < self.config.participation_rate:
            participation_rate = min(
                self.config.max_participation_rate,
                self.config.participation_rate * 1.2
            )
            
        target_size = current_volume * participation_rate
        
        # Ensure we don't exceed target position
        remaining_quantity = (self.config.target_position - 
                            self.position.quantity)
        
        return min(target_size, remaining_quantity)
        
    def on_market_update(self, price: float, volume: float, timestamp: datetime):
        """Handle market updates and execute VWAP strategy."""
        self.update_position(price)
        
        # Check if we're within trading window
        if not (self.start_time <= timestamp.time() <= self.end_time):
            return
            
        # Update history
        self.volume_history.append(volume)
        self.price_volume_history.append((price, volume))
        self.total_volume += volume
        
        # Calculate VWAP
        vwap = self.calculate_vwap()
        if vwap is None:
            return
            
        # Calculate target trade size
        target_size = self.calculate_target_trade_size(volume)
        
        if target_size > 0:
            # Adjust trade size based on price relative to VWAP
            price_deviation = (price - vwap) / vwap
            
            if abs(self.config.target_position) > 0:
                # If buying, prefer to buy below VWAP
                if self.config.target_position > 0 and price_deviation > 0.01:
                    target_size *= 0.5
                # If selling, prefer to sell above VWAP
                elif self.config.target_position < 0 and price_deviation < -0.01:
                    target_size *= 0.5
                    
            if self.execute_trade(price, target_size, timestamp):
                self.participation_volume += abs(target_size)