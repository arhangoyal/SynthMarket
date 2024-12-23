from dataclasses import dataclass, field
from typing import Optional

@dataclass
class BaseConfig:
    initial_capital: float = 1000000.0
    max_position_size: float = 1000.0
    risk_limit: float = 100000.0

@dataclass
class MarketMakerConfig(BaseConfig):
    spread_width: float = 0.02  # 2% spread
    inventory_target: float = 0.0
    max_inventory: float = 100.0
    min_trade_size: float = 1.0
    max_trade_size: float = 10.0

@dataclass
class StatArbConfig(BaseConfig):
    lookback_period: int = 100
    entry_threshold: float = 2.0  # Z-score threshold for entry
    exit_threshold: float = 0.0   # Z-score threshold for exit
    position_size: float = 10.0

@dataclass
class PositionTakerConfig(BaseConfig):
    momentum_period: int = 20
    volatility_period: int = 20
    entry_threshold: float = 0.02  # 2% price movement
    stop_loss: float = 0.05       # 5% stop loss
    take_profit: float = 0.1      # 10% take profit

@dataclass
class TWAPConfig(BaseConfig):
    target_position: float = field(default=0.0)  # Provide a sensible default
    start_time: str = field(default="09:30:00")  # Default start time
    end_time: str = field(default="16:00:00")    # Default end time
    num_slices: int = 10
    deviation_threshold: float = 0.02  # Max price deviation allowed

@dataclass
class VWAPConfig(BaseConfig):
    target_position: float = field(default=0.0)  # Provide a sensible default
    start_time: str = field(default="09:30:00")  # Default start time
    end_time: str = field(default="16:00:00")    # Default end time
    participation_rate: float = 0.1  # Target 10% of volume
    max_participation_rate: float = 0.3  # Maximum 30% of volume