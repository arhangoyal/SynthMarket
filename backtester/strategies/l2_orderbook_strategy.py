# strategies/l2_orderbook_strategy.py
from typing import Dict, Any, Optional, Tuple
from utils.orderbook import OrderBook

class L2OrderbookStrategy:
    def __init__(self, parameters: Dict[str, Any] = None):
        """
        Initialize strategy with parameters
        
        Args:
            parameters: Dictionary containing:
                - position_limit: Maximum allowed position size
                - imbalance_threshold: Threshold for orderbook imbalance signals
                - trade_size: Size of each trade
        """
        self.parameters = parameters or {}
        self.position_limit = self.parameters.get('position_limit', 100)
        self.imbalance_threshold = self.parameters.get('imbalance_threshold', 0.3)
        self.trade_size = self.parameters.get('trade_size', 1.0)
        self.position = 0
        self.trades = []
        
    def calculate_orderbook_imbalance(self, market_depth: Dict) -> float:
        """Calculate order book imbalance from L2 data"""
        bid_volume = sum(market_depth[f'BidSize_{i}'] for i in range(1, 6))
        ask_volume = sum(market_depth[f'AskSize_{i}'] for i in range(1, 6))
        
        if bid_volume + ask_volume == 0:
            return 0.0
            
        return (bid_volume - ask_volume) / (bid_volume + ask_volume)
        
    def generate_signal(self, market_depth: Dict) -> Tuple[bool, str, float]:
        """
        Generate trading signal based on orderbook imbalance
        
        Returns:
            Tuple of (should_trade, side, size)
            side is either 'buy' or 'sell'
        """
        imbalance = self.calculate_orderbook_imbalance(market_depth)
        
        if abs(imbalance) > self.imbalance_threshold:
            # Check position limits
            if abs(self.position) >= self.position_limit:
                return False, '', 0.0
                
            side = 'buy' if imbalance > 0 else 'sell'
            return True, side, self.trade_size
            
        return False, '', 0.0
        
    def update_position(self, fill_size: float, side: str):
        """Update position after a trade"""
        self.position += fill_size if side == 'buy' else -fill_size