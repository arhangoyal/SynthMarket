# market_participants/utils/metrics.py

import numpy as np
from typing import List, Dict, Optional
from datetime import datetime

class TradingMetrics:
    @staticmethod
    def calculate_returns(prices: List[float]) -> np.ndarray:
        """Calculate log returns from price series."""
        return np.diff(np.log(prices))
        
    @staticmethod
    def calculate_sharpe_ratio(returns: np.ndarray, risk_free_rate: float = 0.0) -> float:
        """Calculate annualized Sharpe ratio."""
        if len(returns) < 2:
            return 0.0
            
        excess_returns = returns - risk_free_rate
        return np.sqrt(252) * (np.mean(excess_returns) / np.std(returns))
        
    @staticmethod
    def calculate_sortino_ratio(returns: np.ndarray, risk_free_rate: float = 0.0) -> float:
        """Calculate Sortino ratio using downside deviation."""
        if len(returns) < 2:
            return 0.0
            
        excess_returns = returns - risk_free_rate
        downside_returns = returns[returns < 0]
        downside_std = np.std(downside_returns) if len(downside_returns) > 0 else 0
        
        return np.sqrt(252) * (np.mean(excess_returns) / downside_std) if downside_std != 0 else 0
        
    @staticmethod
    def calculate_max_drawdown(prices: List[float]) -> float:
        """Calculate maximum drawdown from peak."""
        peaks = np.maximum.accumulate(prices)
        drawdowns = (peaks - prices) / peaks
        return np.max(drawdowns)
        
    @staticmethod
    def calculate_win_rate(trades: List[Dict]) -> float:
        """Calculate win rate from trade history."""
        if not trades:
            return 0.0
            
        profitable_trades = sum(1 for trade in trades if trade.get('pnl', 0) > 0)
        return profitable_trades / len(trades)
        
    @staticmethod
    def calculate_profit_factor(trades: List[Dict]) -> float:
        """Calculate profit factor (gross profit / gross loss)."""
        gross_profit = sum(trade['pnl'] for trade in trades if trade.get('pnl', 0) > 0)
        gross_loss = abs(sum(trade['pnl'] for trade in trades if trade.get('pnl', 0) < 0))
        
        return gross_profit / gross_loss if gross_loss != 0 else float('inf')
        
    @staticmethod
    def calculate_vwap(prices: List[float], volumes: List[float]) -> float:
        """Calculate Volume Weighted Average Price."""
        if not prices or not volumes or len(prices) != len(volumes):
            return 0.0
            
        return np.sum(np.multiply(prices, volumes)) / np.sum(volumes)
        
    @staticmethod
    def calculate_volatility(returns: np.ndarray, annualize: bool = True) -> float:
        """Calculate return volatility."""
        vol = np.std(returns)
        return vol * np.sqrt(252) if annualize else vol
        
    @staticmethod
    def calculate_var(returns: np.ndarray, confidence: float = 0.95) -> float:
        """Calculate Value at Risk."""
        return np.percentile(returns, (1 - confidence) * 100)
        
    @staticmethod
    def calculate_expected_shortfall(returns: np.ndarray, confidence: float = 0.95) -> float:
        """Calculate Expected Shortfall (Conditional VaR)."""
        var = np.percentile(returns, (1 - confidence) * 100)
        return np.mean(returns[returns <= var])
        
    @staticmethod
    def calculate_beta(returns: np.ndarray, market_returns: np.ndarray) -> float:
        """Calculate beta relative to market returns."""
        if len(returns) != len(market_returns):
            return 0.0
        covariance = np.cov(returns, market_returns)[0][1]
        market_variance = np.var(market_returns)
        return covariance / market_variance if market_variance != 0 else 0
        
    @staticmethod
    def calculate_information_ratio(returns: np.ndarray, benchmark_returns: np.ndarray) -> float:
        """Calculate Information Ratio."""
        if len(returns) != len(benchmark_returns):
            return 0.0
        active_returns = returns - benchmark_returns
        return np.mean(active_returns) / np.std(active_returns) if np.std(active_returns) != 0 else 0
        
    @staticmethod
    def calculate_calmar_ratio(returns: np.ndarray, prices: List[float]) -> float:
        """Calculate Calmar Ratio (annual return / max drawdown)."""
        if len(returns) < 1 or len(prices) < 2:
            return 0.0
        annual_return = np.mean(returns) * 252
        max_drawdown = TradingMetrics.calculate_max_drawdown(prices)
        return annual_return / max_drawdown if max_drawdown != 0 else float('inf')
        
    @staticmethod
    def calculate_trade_statistics(trades: List[Dict]) -> Dict:
        """Calculate comprehensive trade statistics."""
        if not trades:
            return {}
            
        pnls = [trade.get('pnl', 0) for trade in trades]
        profitable_trades = [pnl for pnl in pnls if pnl > 0]
        loss_trades = [pnl for pnl in pnls if pnl < 0]
        
        return {
            'total_trades': len(trades),
            'profitable_trades': len(profitable_trades),
            'loss_trades': len(loss_trades),
            'win_rate': len(profitable_trades) / len(trades) if trades else 0,
            'average_profit': np.mean(profitable_trades) if profitable_trades else 0,
            'average_loss': np.mean(loss_trades) if loss_trades else 0,
            'largest_profit': max(profitable_trades) if profitable_trades else 0,
            'largest_loss': min(loss_trades) if loss_trades else 0,
            'total_pnl': sum(pnls),
            'profit_factor': abs(sum(profitable_trades) / sum(loss_trades)) if loss_trades else float('inf'),
            'average_trade_pnl': np.mean(pnls) if pnls else 0,
            'pnl_std': np.std(pnls) if pnls else 0
        }
        
    @staticmethod
    def calculate_position_metrics(positions: List[Dict]) -> Dict:
        """Calculate position-related metrics."""
        if not positions:
            return {}
            
        position_sizes = [abs(pos.get('quantity', 0)) for pos in positions]
        holding_periods = [
            (pos.get('exit_time', datetime.now()) - pos.get('entry_time')).total_seconds() / 3600 
            for pos in positions if pos.get('entry_time')
        ]
        
        return {
            'avg_position_size': np.mean(position_sizes),
            'max_position_size': max(position_sizes),
            'min_position_size': min(position_sizes),
            'position_size_std': np.std(position_sizes),
            'avg_holding_period': np.mean(holding_periods) if holding_periods else 0,
            'max_holding_period': max(holding_periods) if holding_periods else 0,
            'min_holding_period': min(holding_periods) if holding_periods else 0,
            'holding_period_std': np.std(holding_periods) if holding_periods else 0
        }
        
    @staticmethod
    def calculate_drawdown_metrics(prices: List[float]) -> Dict:
        """Calculate drawdown-related metrics."""
        if len(prices) < 2:
            return {}
            
        peaks = np.maximum.accumulate(prices)
        drawdowns = (peaks - prices) / peaks
        
        return {
            'max_drawdown': np.max(drawdowns),
            'avg_drawdown': np.mean(drawdowns),
            'drawdown_std': np.std(drawdowns),
            'current_drawdown': drawdowns[-1]
        }
        
    @staticmethod
    def calculate_risk_metrics(returns: np.ndarray, prices: List[float]) -> Dict:
        """Calculate comprehensive risk metrics."""
        if len(returns) < 2:
            return {}
            
        return {
            'volatility': TradingMetrics.calculate_volatility(returns),
            'var_95': TradingMetrics.calculate_var(returns),
            'var_99': TradingMetrics.calculate_var(returns, 0.99),
            'expected_shortfall_95': TradingMetrics.calculate_expected_shortfall(returns),
            'expected_shortfall_99': TradingMetrics.calculate_expected_shortfall(returns, 0.99),
            'skewness': float(np.nan) if len(returns) < 2 else float(stats.skew(returns)),
            'kurtosis': float(np.nan) if len(returns) < 2 else float(stats.kurtosis(returns)),
            **TradingMetrics.calculate_drawdown_metrics(prices)
        }
        
    @classmethod
    def generate_performance_report(cls, 
                                  trades: List[Dict],
                                  positions: List[Dict],
                                  returns: np.ndarray,
                                  prices: List[float],
                                  benchmark_returns: Optional[np.ndarray] = None) -> Dict:
        """Generate comprehensive performance report."""
        report = {}
        
        # Trade statistics
        report['trade_metrics'] = cls.calculate_trade_statistics(trades)
        
        # Position metrics
        report['position_metrics'] = cls.calculate_position_metrics(positions)
        
        # Risk metrics
        report['risk_metrics'] = cls.calculate_risk_metrics(returns, prices)
        
        # Return-based metrics
        report['return_metrics'] = {
            'sharpe_ratio': cls.calculate_sharpe_ratio(returns),
            'sortino_ratio': cls.calculate_sortino_ratio(returns),
            'calmar_ratio': cls.calculate_calmar_ratio(returns, prices),
            'annualized_return': np.mean(returns) * 252,
            'annualized_volatility': cls.calculate_volatility(returns),
            'total_return': (prices[-1] / prices[0] - 1) if len(prices) > 1 else 0
        }
        
        # Benchmark-relative metrics (if provided)
        if benchmark_returns is not None:
            report['benchmark_metrics'] = {
                'beta': cls.calculate_beta(returns, benchmark_returns),
                'information_ratio': cls.calculate_information_ratio(returns, benchmark_returns),
                'correlation': np.corrcoef(returns, benchmark_returns)[0, 1],
                'tracking_error': np.std(returns - benchmark_returns) * np.sqrt(252)
            }
            
        return report