# market_participants/traders/twap.py

from datetime import datetime, time
import numpy as np
from ..base.participant import Participant
from ..configs.participant_configs import TWAPConfig

class TWAPTrader(Participant):
    def __init__(self, config: TWAPConfig):
        super().__init__(
            initial_capital=config.initial_capital,
            max_position_size=config.max_position_size,
            risk_limit=config.risk_limit
        )
        self.config = config
        self.slice_size = config.target_position / config.num_slices
        self.executed_slices = 0
        self.last_execution_time = None
        
        # Parse trading window times
        self.start_time = datetime.strptime(config.start_time, "%H:%M:%S").time()
        self.end_time = datetime.strptime(config.end_time, "%H:%M:%S").time()
        
        # Calculate time per slice
        start_seconds = self._time_to_seconds(self.start_time)
        end_seconds = self._time_to_seconds(self.end_time)
        self.seconds_per_slice = (end_seconds - start_seconds) / config.num_slices
        
    @staticmethod
    def _time_to_seconds(t: time) -> int:
        """Convert time to seconds since midnight."""
        return t.hour * 3600 + t.minute * 60 + t.second
        
    def _should_execute_slice(self, current_time: datetime) -> bool:
        """Determine if it's time to execute the next slice."""
        if self.executed_slices >= self.config.num_slices:
            return False
            
        current_seconds = self._time_to_seconds(current_time.time())
        start_seconds = self._time_to_seconds(self.start_time)
        
        # Calculate expected slices by now
        expected_slices = int((current_seconds - start_seconds) / self.seconds_per_slice)
        
        return expected_slices > self.executed_slices
        
    def _calculate_slice_size(self, current_price: float) -> float:
        """Calculate the size of the next slice, adjusting for price deviation."""
        base_slice_size = self.slice_size
        
        if len(self.trades) > 0:
            # Calculate price deviation from VWAP
            quantities = [trade['quantity'] for trade in self.trades]
            prices = [trade['price'] for trade in self.trades]
            vwap = np.average(prices, weights=quantities)
            
            # Adjust slice size based on price deviation
            price_deviation = abs(current_price - vwap) / vwap
            if price_deviation > self.config.deviation_threshold:
                # Reduce slice size if price has deviated significantly
                return base_slice_size * 0.5
                
        return base_slice_size
        
    def on_market_update(self, price: float, volume: float, timestamp: datetime):
        """Handle market updates and execute TWAP strategy."""
        self.update_position(price)
        
        # Check if we're within trading window
        if not (self.start_time <= timestamp.time() <= self.end_time):
            return
            
        # Check if we should execute next slice
        if self._should_execute_slice(timestamp):
            slice_size = self._calculate_slice_size(price)
            
            # Ensure we don't exceed target position
            remaining_quantity = (self.config.target_position - 
                               self.position.quantity)
            slice_size = min(slice_size, remaining_quantity)
            
            if abs(slice_size) > 0:
                if self.execute_trade(price, slice_size, timestamp):
                    self.executed_slices += 1
                    self.last_execution_time = timestamp