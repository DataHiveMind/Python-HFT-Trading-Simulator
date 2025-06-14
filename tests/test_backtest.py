# tests/test_backtest.py
import pandas as pd
from hft_simulator.core.execution import ExecutionEngine
from hft_simulator.core.backtest import Backtester

def test_performance_metrics():
    engine = ExecutionEngine()
    backtester = Backtester(engine)
    
    # Simulate a sequence of orders
    orders = [
        ("BUY", 100, 10),  # Position increases
        ("SELL", 101, 10)  # Position decreases, yielding a profit
    ]
    for order in orders:
        engine.send_order(*order)
        backtester.record_trade(order)
    
    metrics = backtester.performance_metrics()
    # Validate that PnL calculation is in the expected format and Sharpe ratio is numeric
    assert "PnL" in metrics
    assert "Sharpe" in metrics
    assert isinstance(metrics["PnL"], (float, int))
    assert isinstance(metrics["Sharpe"], (float, int))
